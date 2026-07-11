import json

import pytest

from badgegen import generate, manifest
from badgegen.config import Settings
from tests.conftest import png_bytes


class FakeProvider:
    name = "fake"
    model = "fake-1"

    def __init__(self, images):
        self.images = images
        self.calls = []

    def generate(self, prompt, reference_images, n=1):
        self.calls.append((prompt, len(reference_images), n))
        return self.images[:n]


def _manifest():
    return manifest.Manifest(
        style="ESTILO",
        reference_images=["badge-template.png"],
        badges=[
            manifest.Badge(slug="badge-a", name="Laser Hero", file="badge-a.png",
                           description="desc a", visual="cabezal láser", status="missing"),
            manifest.Badge(slug="badge-b", name="B", file="badge-b.png",
                           description="desc b", status="ok"),
            manifest.Badge(slug="badge-c", name="C", file="badge-c.png",
                           description="desc c", status="regen", prompt_extra="EXTRA-C"),
        ],
    )


def test_build_prompt_contents():
    m = _manifest()
    p = generate.build_prompt(m, m.get("badge-a"))
    assert "ESTILO" in p and "Laser Hero" in p and "cabezal láser" in p
    assert "perfect circle" in p.lower()
    pc = generate.build_prompt(m, m.get("badge-c"))
    assert "desc c" in pc  # sin visual cae a description
    assert "EXTRA-C" in pc


def test_select_badges():
    m = _manifest()
    assert [b.slug for b in generate.select_badges(m, None, ["missing", "regen"])] == ["badge-a", "badge-c"]
    assert [b.slug for b in generate.select_badges(m, ["badge-b"], None)] == ["badge-b"]
    assert generate.select_badges(m, None, None) == []


def test_run_generate_writes_candidates_and_sidecars(tmp_path, make_badge):
    settings = Settings(repo_root=tmp_path)
    (tmp_path / "badge-template.png").write_bytes(png_bytes(make_badge(w=200, h=200, rx=80, ry=80)))
    good = png_bytes(make_badge())
    provider = FakeProvider([good, good])
    m = _manifest()
    report = generate.run_generate(settings, m, provider, statuses=["missing"], n=2)
    files = report["badge-a"]
    assert len(files) == 2
    d = tmp_path / "candidates" / "badge-a"
    assert (d / "01-fake.png").is_file() and (d / "02-fake.png").is_file()
    sidecar = json.loads((d / "01-fake.json").read_text())
    assert sidecar["provider"] == "fake" and sidecar["model"] == "fake-1"
    assert "ESTILO" in sidecar["prompt"]
    assert sidecar["qc"]["roundness"] > 0.99 and sidecar["qc"]["issues"] == []
    # segunda tanda continúa numeración
    generate.run_generate(settings, m, provider, slugs=["badge-a"], n=1)
    assert (d / "03-fake.png").is_file()


def test_run_generate_honors_badge_provider_override(tmp_path, monkeypatch, make_badge):
    settings = Settings(repo_root=tmp_path)
    good = png_bytes(make_badge())
    provider = FakeProvider([good])

    fake2 = FakeProvider([good])
    fake2.name = "fake2"
    fake2.model = "fake2-1"

    def fake_get_provider(name, model=None):
        assert name == "fake2"
        return fake2

    monkeypatch.setattr("badgegen.providers.get_provider", fake_get_provider)

    m = _manifest()
    m.get("badge-a").provider = "fake2"
    report = generate.run_generate(settings, m, provider, statuses=["missing", "regen"], n=1)
    assert len(report["badge-a"]) == 1 and len(report["badge-c"]) == 1
    d = tmp_path / "candidates"
    assert (d / "badge-a" / "01-fake2.png").is_file()
    assert (d / "badge-c" / "01-fake.png").is_file()
    assert len(fake2.calls) == 1  # solo badge-a usó el override
    assert len(provider.calls) == 1  # badge-c siguió con el provider global


def test_run_generate_batch_survives_provider_error(tmp_path):
    settings = Settings(repo_root=tmp_path)

    class Boom(FakeProvider):
        def generate(self, *a, **kw):
            raise RuntimeError("api caída")

    m = _manifest()
    report = generate.run_generate(settings, m, Boom([]), statuses=["missing", "regen"], n=1)
    assert "api caída" in report["badge-a"] and "api caída" in report["badge-c"]


def test_select_badges_unknown_slug_raises():
    m = _manifest()
    with pytest.raises(KeyError, match="badge-zz"):
        generate.select_badges(m, ["badge-zz"], None)


def test_run_generate_small_candidate_wrong_size_is_informative(tmp_path, make_badge):
    settings = Settings(repo_root=tmp_path)
    small = png_bytes(make_badge(w=1024, h=1024, rx=450, ry=450))
    provider = FakeProvider([small])
    m = _manifest()
    report = generate.run_generate(settings, m, provider, slugs=["badge-a"], n=1)
    assert len(report["badge-a"]) == 1  # se guardó a pesar del wrong-size
    import json as _json
    sidecar = _json.loads((tmp_path / "candidates" / "badge-a" / "01-fake.json").read_text())
    assert "wrong-size" in sidecar["qc"]["issues"]
    assert sidecar["qc"]["roundness"] > 0.99


def test_badge_references_override_and_fallback(tmp_path, make_badge):
    settings = Settings(repo_root=tmp_path)
    (tmp_path / "global-ref.png").write_bytes(b"GLOBAL")
    (tmp_path / "serie-n1.png").write_bytes(b"SERIE")
    m = manifest.Manifest(reference_images=["global-ref.png"], badges=[])

    con_serie = manifest.Badge(slug="badge-s2", name="S2", file="s2.png",
                               references=["serie-n1.png"])
    sin_serie = manifest.Badge(slug="badge-x", name="X", file="x.png")
    serie_inexistente = manifest.Badge(slug="badge-s3", name="S3", file="s3.png",
                                       references=["serie-n2-aun-no-existe.png"])

    assert generate.badge_references(settings, m, con_serie) == [b"SERIE"]
    assert generate.badge_references(settings, m, sin_serie) == [b"GLOBAL"]
    # la referencia de serie aún no está promocionada -> cae a las globales
    assert generate.badge_references(settings, m, serie_inexistente) == [b"GLOBAL"]


def test_manifest_roundtrip_references(tmp_path):
    m = manifest.Manifest(badges=[
        manifest.Badge(slug="badge-a", name="A", file="a.png", references=["ref.png"]),
        manifest.Badge(slug="badge-b", name="B", file="b.png"),
    ])
    p = tmp_path / "badges.yaml"
    manifest.save(m, p)
    m2 = manifest.load(p)
    assert m2.get("badge-a").references == ["ref.png"]
    assert m2.get("badge-b").references is None
    assert "references" not in p.read_text().split("badge-b")[1]
