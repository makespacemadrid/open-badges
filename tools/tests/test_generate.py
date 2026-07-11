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
