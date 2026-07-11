import threading

import httpx
import pytest
from PIL import Image

from badgegen import docs_gen, manifest, promote, serve
from badgegen.config import Settings
from tests.conftest import png_bytes


@pytest.fixture
def repo(tmp_path, make_badge, monkeypatch):
    settings = Settings(repo_root=tmp_path)
    manifest.save(manifest.Manifest(badges=[
        manifest.Badge(slug="badge-a", name="A", file="badge-a.png", status="missing"),
    ]), settings.manifest_path)
    for name in ("README.md", "missing-images.md"):
        (tmp_path / name).write_text(
            f"x\n\n{docs_gen.START}\n{docs_gen.END}\n", encoding="utf-8")
    cand = tmp_path / "candidates" / "badge-a" / "01-gemini.png"
    cand.parent.mkdir(parents=True)
    cand.write_bytes(png_bytes(make_badge(rx=560, ry=545)))
    monkeypatch.setattr(promote, "purge_cdn", lambda *a, **kw: True)
    return settings


@pytest.fixture
def server(repo):
    srv = serve.make_server(repo, port=0)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    yield base, repo
    srv.shutdown()
    srv.server_close()


def test_gallery_page_lists_candidates(server):
    base, _ = server
    r = httpx.get(f"{base}/")
    assert r.status_code == 200
    assert "badge-a" in r.text
    assert "/img?p=candidates/badge-a/01-gemini.png" in r.text
    assert "Promocionar" in r.text


def test_img_serves_png_and_blocks_traversal(server, repo):
    base, settings = server
    ok = httpx.get(f"{base}/img", params={"p": "candidates/badge-a/01-gemini.png"})
    assert ok.status_code == 200 and ok.headers["content-type"] == "image/png"
    (settings.repo_root.parent / "fuera.png").write_bytes(b"png")
    bad = httpx.get(f"{base}/img", params={"p": "../fuera.png"})
    assert bad.status_code == 404
    bad2 = httpx.get(f"{base}/img", params={"p": "badges.yaml"})
    assert bad2.status_code == 404


def test_promote_button_flow(server, repo):
    base, settings = server
    r = httpx.post(f"{base}/promote",
                   data={"slug": "badge-a", "candidate": "candidates/badge-a/01-gemini.png"})
    assert r.status_code == 303
    assert "ok=badge-a" in r.headers["location"]
    final = settings.repo_root / "badge-a.png"
    assert final.is_file() and Image.open(final).size == (1254, 1254)
    assert manifest.load(settings.manifest_path).get("badge-a").status == "ok"
    # la página ya no lista candidatos
    page = httpx.get(f"{base}/", follow_redirects=True)
    assert "01-gemini" not in page.text


def test_promote_invalid_candidate_redirects_with_error(server):
    base, _ = server
    r = httpx.post(f"{base}/promote",
                   data={"slug": "badge-a", "candidate": "../../etc/passwd"})
    assert r.status_code == 303
    assert "err=" in r.headers["location"]


def test_page_groups_by_track_with_context(server, repo, make_badge):
    # añade al track un badge existente como contexto
    m = manifest.load(repo.manifest_path)
    m.badges[0].track = "maquinas"
    m.badges.append(manifest.Badge(slug="badge-viejo", name="Viejo", file="badge-viejo.png",
                                   track="maquinas", status="ok"))
    manifest.save(m, repo.manifest_path)
    (repo.repo_root / "badge-viejo.png").write_bytes(png_bytes(make_badge()))
    base, _ = server
    page = httpx.get(f"{base}/").text
    assert "Máquinas" in page                       # título del track
    assert "/img?p=badge-viejo.png" in page          # tira de contexto
    assert "ya en el track" in page
    assert "＋3 sugerencias" in page                 # botón de más candidatos


def test_generate_more_via_ui(server, repo, monkeypatch, make_badge):
    base, settings = server
    calls = {}

    def fake_generate(s, slug):
        calls["slug"] = slug
        cand = s.candidates_dir / slug / "99-gemini.png"
        cand.write_bytes(png_bytes(make_badge()))

    monkeypatch.setattr(serve, "_generate_more", fake_generate)
    r = httpx.post(f"{base}/generate", data={"slug": "badge-a"})
    assert r.status_code == 303
    import time

    jobs = None
    for _ in range(40):  # espera a que el hilo termine
        page = httpx.get(f"{base}/").text
        if "99-gemini" in page:
            break
        time.sleep(0.05)
    assert calls["slug"] == "badge-a"
    assert "99-gemini" in page


def test_generate_error_shown(server, repo, monkeypatch):
    base, _ = server

    def boom(s, slug):
        raise RuntimeError("proveedor caído")

    monkeypatch.setattr(serve, "_generate_more", boom)
    httpx.post(f"{base}/generate", data={"slug": "badge-a"})
    import time

    for _ in range(40):
        page = httpx.get(f"{base}/").text
        if "proveedor caído" in page:
            break
        time.sleep(0.05)
    assert "ERROR" in page and "proveedor caído" in page
