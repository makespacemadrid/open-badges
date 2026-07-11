import httpx
import pytest
from PIL import Image

from badgegen import docs_gen, manifest, promote
from badgegen.config import Settings
from tests.conftest import png_bytes


def _repo(tmp_path, make_badge):
    settings = Settings(repo_root=tmp_path)
    m = manifest.Manifest(badges=[
        manifest.Badge(slug="badge-a", name="A", file="badge-a.png",
                       status="regen", issues=["flattened-circle"]),
    ])
    for name in ("README.md", "missing-images.md"):
        (tmp_path / name).write_text(
            f"x\n\n{docs_gen.START}\n{docs_gen.END}\n", encoding="utf-8")
    cand = tmp_path / "candidates" / "badge-a" / "01-gemini.png"
    cand.parent.mkdir(parents=True)
    cand.write_bytes(png_bytes(make_badge(rx=560, ry=540)))  # achatado corregible
    return settings, m, cand


def _client(record):
    def handler(request):
        record.append(str(request.url))
        return httpx.Response(200, text="purged")

    return httpx.Client(transport=httpx.MockTransport(handler))


def test_promote_full_flow(tmp_path, make_badge):
    settings, m, cand = _repo(tmp_path, make_badge)
    purges = []
    out = promote.promote(settings, m, "badge-a", cand, client=_client(purges))
    assert out == tmp_path / "badge-a.png" and out.is_file()
    im = Image.open(out)
    assert im.size == (1254, 1254)
    badge = m.get("badge-a")
    assert badge.status == "ok" and badge.issues == []
    assert not (tmp_path / "candidates" / "badge-a").exists()
    assert purges == ["https://purge.jsdelivr.net/gh/makespacemadrid/open-badges@main/badge-a.png"]
    assert "badge-a" in (tmp_path / "README.md").read_text(encoding="utf-8")
    # el manifiesto quedó persistido
    assert manifest.load(settings.manifest_path).get("badge-a").status == "ok"


def test_promote_keep_candidates(tmp_path, make_badge):
    settings, m, cand = _repo(tmp_path, make_badge)
    promote.promote(settings, m, "badge-a", cand, keep=True, client=_client([]))
    assert cand.is_file()


def test_promote_unknown_slug_and_missing_candidate(tmp_path, make_badge):
    settings, m, cand = _repo(tmp_path, make_badge)
    with pytest.raises(KeyError):
        promote.promote(settings, m, "badge-zz", cand, client=_client([]))
    with pytest.raises(FileNotFoundError):
        promote.promote(settings, m, "badge-a", tmp_path / "no.png", client=_client([]))


def test_purge_failure_does_not_abort(tmp_path, make_badge):
    settings, m, cand = _repo(tmp_path, make_badge)

    def handler(request):
        return httpx.Response(500)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    out = promote.promote(settings, m, "badge-a", cand, client=client)
    assert out.is_file()  # el flujo terminó igualmente


def test_fix_in_place(tmp_path, make_badge):
    settings, m, _ = _repo(tmp_path, make_badge)
    final = tmp_path / "badge-a.png"
    final.write_bytes(png_bytes(make_badge(rx=560, ry=536)))  # achatado como los reales
    purges = []
    promote.fix(settings, m, "badge-a", client=_client(purges))
    from badgegen import postprocess

    assert postprocess.analyze(Image.open(final)).ratio > 0.99
    assert m.get("badge-a").status == "ok"
    assert purges  # también purga
