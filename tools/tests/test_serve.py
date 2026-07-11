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
    m.badges[0].category = "maquinas"
    m.badges.append(manifest.Badge(slug="badge-viejo", name="Viejo", file="badge-viejo.png",
                                   category="maquinas", status="ok"))
    manifest.save(m, repo.manifest_path)
    (repo.repo_root / "badge-viejo.png").write_bytes(png_bytes(make_badge()))
    base, _ = server
    page = httpx.get(f"{base}/").text
    assert "Máquinas" in page                        # título de la sección
    assert "/img?p=badge-viejo.png" in page          # el badge hecho, como fila verde
    assert "Regenerar" in page and "Fix círculo" in page  # acciones sobre badges ok
    assert "＋3 sugerencias" in page                 # botón de más candidatos


def test_generate_more_via_ui(server, repo, monkeypatch, make_badge):
    base, settings = server
    calls = {}

    def fake_generate(s, slug, provider=None):
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

    def boom(s, slug, provider=None):
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


def test_tracks_render_as_actionable_ladders(server, repo, make_badge):
    # todos los tracks se ven siempre, nivel a nivel, con acciones inline
    m = manifest.load(repo.manifest_path)
    m.badges.append(manifest.Badge(slug="badge-n1", name="Nivel Uno", file="badge-n1.png",
                                   category="comunidad", track="purchases", track_level=1,
                                   status="ok"))
    m.badges.append(manifest.Badge(slug="badge-n2", name="Nivel Dos", file="badge-n2.png",
                                   category="comunidad", track="purchases", track_level=2,
                                   status="missing", references=["badge-n1-inexistente.png"]))
    manifest.save(m, repo.manifest_path)
    (repo.repo_root / "badge-n1.png").write_bytes(png_bytes(make_badge()))
    base, _ = server
    page = httpx.get(f"{base}/").text
    assert "Compras" in page                          # título del track
    assert "1/2 con imagen" in page                   # progreso
    assert "/img?p=badge-n1.png" in page              # nivel 1 con imagen
    assert "lvl 2" in page and "Nivel Dos" in page    # nivel 2 listado en orden
    assert "Generar 3 candidatos" in page             # acción para el nivel sin candidatos
    assert "su nivel anterior aún no tiene imagen" in page  # aviso de referencias


def test_api_state_json(server, repo):
    base, _ = server
    r = httpx.get(f"{base}/api/state")
    assert r.status_code == 200
    state = r.json()
    assert state["counts"]["missing"] == 1
    badge = next(b for b in state["badges"] if b["slug"] == "badge-a")
    assert len(badge["candidates"]) == 1
    assert "style" in state and "tracks" in state


def test_edit_badge_prompt_via_ui(server, repo):
    base, settings = server
    r = httpx.post(f"{base}/edit", data={
        "slug": "badge-a", "visual": "un robot saludando",
        "prompt_extra": "  ", "references": "assets/x.png\n\nbadge-y.png"})
    assert r.status_code == 303 and "ok=" in r.headers["location"]
    b = manifest.load(settings.manifest_path).get("badge-a")
    assert b.visual == "un robot saludando"
    assert b.prompt_extra is None
    assert b.references == ["assets/x.png", "badge-y.png"]


def test_edit_track_config_via_ui(server, repo):
    base, settings = server
    r = httpx.post(f"{base}/track", data={
        "track": "eldership", "references": "assets/makespace-icon.png",
        "prompt_extra": "motivo: el logo M"})
    assert r.status_code == 303
    m = manifest.load(settings.manifest_path)
    assert m.tracks["eldership"].references == ["assets/makespace-icon.png"]
    assert m.tracks["eldership"].prompt_extra == "motivo: el logo M"
    # vaciar la config la elimina
    httpx.post(f"{base}/track", data={"track": "eldership", "references": "", "prompt_extra": ""})
    assert "eldership" not in manifest.load(settings.manifest_path).tracks


def test_edit_globals_via_ui(server, repo):
    base, settings = server
    httpx.post(f"{base}/globals", data={"style": "nuevo estilo global",
                                        "references": "badge-uno.png\nbadge-dos.png"})
    m = manifest.load(settings.manifest_path)
    assert m.style == "nuevo estilo global"
    assert m.reference_images == ["badge-uno.png", "badge-dos.png"]


def test_fix_via_ui(server, repo, make_badge):
    base, settings = server
    m = manifest.load(settings.manifest_path)
    m.badges.append(manifest.Badge(slug="badge-oval", name="Oval", file="badge-oval.png",
                                   status="ok"))
    manifest.save(m, settings.manifest_path)
    (settings.repo_root / "badge-oval.png").write_bytes(png_bytes(make_badge(rx=560, ry=540)))
    r = httpx.post(f"{base}/fix", data={"slug": "badge-oval"})
    assert r.status_code == 303 and "ok=" in r.headers["location"]
    from badgegen import postprocess

    assert postprocess.analyze(Image.open(settings.repo_root / "badge-oval.png")).ratio > 0.99


def test_scan_via_ui(server, repo, make_badge):
    base, settings = server
    m = manifest.load(settings.manifest_path)
    m.badges.append(manifest.Badge(slug="badge-chato", name="Chato", file="badge-chato.png",
                                   status="ok"))
    manifest.save(m, settings.manifest_path)
    (settings.repo_root / "badge-chato.png").write_bytes(png_bytes(make_badge(rx=560, ry=530)))
    assert httpx.post(f"{base}/scan", data={}).status_code == 303
    import time

    for _ in range(60):
        b = manifest.load(settings.manifest_path).get("badge-chato")
        if b.issues:
            break
        time.sleep(0.1)
    assert "flattened-circle" in b.issues


def test_sync_via_ui(server, repo, monkeypatch):
    base, settings = server
    cat = settings.repo_root / "catalog.ts"
    cat.write_text("""
const BADGES: BadgeSpec[] = [
  {
    slug: 'badge-nuevo',
    name: 'Nuevo',
    description: 'd',
    criteria: 'c',
    categorySlug: 'maquinas',
    achievementType: 'Achievement',
  },
];
""", encoding="utf-8")
    monkeypatch.setenv("BADGEGEN_CATALOG", str(cat))
    r = httpx.post(f"{base}/sync", data={})
    assert r.status_code == 303 and "ok=" in r.headers["location"]
    assert manifest.load(settings.manifest_path).get("badge-nuevo") is not None
