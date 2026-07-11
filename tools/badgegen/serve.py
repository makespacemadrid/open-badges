"""Servidor local de revisión: galería con botón Promocionar, sin copy-paste.

Solo stdlib. Cada POST /promote ejecuta el promote completo (post-proceso,
manifiesto, purge, docs); POST /generate lanza en un hilo la generación de
más candidatos para un badge. La página agrupa por track y muestra los
badges ya existentes de cada track como contexto visual.
"""
from __future__ import annotations

import html
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from badgegen import gallery, manifest as manifest_mod, promote as promote_mod
from badgegen.config import Settings
from badgegen.docs_gen import CATEGORIES

_SERVE_CSS = gallery._CSS + """
.banner{background:#1c5c2e;padding:.5rem 1rem;border-radius:8px;margin-bottom:1rem}
.banner.err{background:#7a2020}
form{display:inline}
button.promote{background:#f5c400;color:#111;font-weight:bold;border:0;
  border-radius:6px;padding:.4rem .8rem}
button.more{background:#333;color:#eee;border:1px solid #555;border-radius:6px;
  padding:.4rem .8rem}
h2.track{border:0;background:#1a1a1a;padding:.6rem 1rem;border-radius:8px;margin-top:2rem}
.context{margin:.3rem 0 1rem}
.context img{width:64px;margin-right:.35rem;vertical-align:middle}
.context .lbl{color:#888;font-size:.85em;margin-right:.6rem}
h3{margin-bottom:.2rem}
.jobs{color:#f5c400}
.badge-name{color:#aaa;font-weight:normal}
"""

_CATEGORY_NAMES = dict(CATEGORIES)

TRACK_TITLES = {
    "eldership": "Antigüedad (años de membresía)",
    "reunion-mensual": "Asambleas mensuales",
    "hack-the-space": "Hack the Space",
    "track-eventos": "Eventos externos",
    "glados-messages": "GLaDOS",
    "ocabra-tokens": "Tokens de oCabra",
    "docmost-pages": "Wiki (Docmost)",
    "purchases": "Compras",
}


def _group_key(badge) -> tuple[str, str]:
    """(clave de agrupación, título): track real si lo hay, si no la categoría."""
    if badge and badge.track:
        return f"track:{badge.track}", TRACK_TITLES.get(badge.track, badge.track)
    category = badge.category if badge else ""
    return f"cat:{category}", _CATEGORY_NAMES.get(category, category or "Otros")


def render_page(settings: Settings, m, items: list[dict], jobs: dict[str, str],
                banner: str = "", error: str = "") -> str:
    parts = []
    refreshing = any(status == "running" for status in jobs.values())
    if banner:
        parts.append(f"<div class='banner'>{html.escape(banner)}</div>")
    if error:
        parts.append(f"<div class='banner err'>{html.escape(error)}</div>")
    if not items and not refreshing:
        parts.append("<p>No quedan candidatos pendientes. 🎉</p>")

    groups: dict[str, dict] = {}
    for item in items:
        badge = m.get(item["slug"])
        key, title = _group_key(badge)
        groups.setdefault(key, {"title": title, "items": []})["items"].append(item)

    for key in sorted(groups, key=lambda k: (not k.startswith("track:"), groups[k]["title"])):
        group = groups[key]
        parts.append(f"<h2 class='track'>{html.escape(group['title'])}</h2>")
        parts.append(_render_context(settings, m, key))
        for item in group["items"]:
            parts.append(_render_badge(m, item, jobs))

    listed = {i["slug"] for i in items}  # jobs recién lanzados sin candidatos aún
    for slug, status in jobs.items():
        if status == "running" and slug not in listed:
            parts.append(f"<p class='jobs'>⏳ generando candidatos de "
                         f"<code>{html.escape(slug)}</code>…</p>")

    refresh = "<meta http-equiv='refresh' content='8'>" if refreshing else ""
    return (
        f"<!doctype html><html><head><meta charset='utf-8'>{refresh}"
        f"<title>badgegen · revisión</title><style>{_SERVE_CSS}</style></head>"
        f"<body><h1>badgegen · revisión de candidatos</h1>{''.join(parts)}</body></html>"
    )


def _render_context(settings: Settings, m, key: str) -> str:
    """Tira de miniaturas del grupo: la escalera en orden de nivel, o la categoría."""
    kind, value = key.split(":", 1)
    if kind == "track":
        members = sorted((b for b in m.badges if b.track == value),
                         key=lambda b: (b.track_level or 0, b.slug))
        thumbs = []
        for b in members:
            level = f"lvl {b.track_level}" if b.track_level is not None else ""
            if b.status == "ok" and (settings.repo_root / b.file).is_file():
                thumbs.append(
                    f"<span title='{html.escape(b.name)} ({level})'>"
                    f"<img src='/img?p={html.escape(b.file)}'></span>"
                )
            else:
                thumbs.append(f"<span class='lbl'>[{html.escape(b.name)} {level}]</span>")
        return (f"<div class='context'><span class='lbl'>escalera completa "
                f"({len(members)} niveles):</span>{''.join(thumbs)}</div>")
    existing = [b for b in m.badges if b.category == value and b.status == "ok"
                and (settings.repo_root / b.file).is_file()]
    if not existing:
        return ""
    thumbs = "".join(
        f"<img src='/img?p={html.escape(b.file)}' title='{html.escape(b.name)}'>"
        for b in existing
    )
    return (f"<div class='context'><span class='lbl'>ya en la categoría "
            f"({len(existing)}):</span>{thumbs}</div>")


def _render_badge(m, item: dict, jobs: dict[str, str]) -> str:
    slug = item["slug"]
    badge = m.get(slug)
    name = badge.name if badge else slug
    level = (f" · nivel {badge.track_level}"
             if badge and badge.track_level is not None else "")
    parts = [f"<h3><code>{html.escape(slug)}</code> "
             f"<span class='badge-name'>— {html.escape(name)}{level}</span></h3>"]
    status = jobs.get(slug, "")
    if status == "running":
        parts.append("<p class='jobs'>⏳ generando más candidatos…</p>")
    elif status.startswith("ERROR"):
        parts.append(f"<div class='banner err'>{html.escape(status)}</div>")
    if item.get("current"):
        parts.append(
            f"<div class='cand'><img src='/img?p={html.escape(item['current'])}' width='180'>"
            f"<div>actual</div></div>"
        )
    for cand in item["candidates"]:
        qc_class = "good" if cand["qc_ok"] else "bad"
        qc_label = "QC ok" if cand["qc_ok"] else "QC ✗"
        parts.append(
            f"<div class='cand'><img src='/img?p={html.escape(cand['file'])}' width='180'>"
            f"<div><span class='qc {qc_class}'>{qc_label}</span> {cand['roundness']:.3f} "
            f"· {html.escape(cand['provider'])}</div>"
            f"<form method='post' action='/promote'>"
            f"<input type='hidden' name='slug' value='{html.escape(slug)}'>"
            f"<input type='hidden' name='candidate' value='{html.escape(cand['file'])}'>"
            f"<button class='promote'>Promocionar ✓</button></form></div>"
        )
    if status != "running":
        parts.append(
            f"<div class='cand'><form method='post' action='/generate'>"
            f"<input type='hidden' name='slug' value='{html.escape(slug)}'>"
            f"<button class='more'>＋3 sugerencias</button></form></div>"
        )
    return "".join(parts)


def _generate_more(settings: Settings, slug: str) -> None:
    """Genera 3 candidatos más para un badge (corre en un hilo)."""
    from badgegen import generate as generate_mod
    from badgegen.providers import get_provider

    m = manifest_mod.load(settings.manifest_path)
    badge = m.get(slug)
    if badge is None:
        raise KeyError(f"slug desconocido: {slug}")
    provider = get_provider(badge.provider)
    report = generate_mod.run_generate(settings, m, provider, slugs=[slug], n=3)
    outcome = report.get(slug)
    if isinstance(outcome, str):
        raise RuntimeError(outcome)


class ReviewHandler(BaseHTTPRequestHandler):
    # inyectados por make_server en la clase derivada:
    settings: Settings
    slugs: list[str] | None
    jobs: dict[str, str]

    def log_message(self, fmt, *args):  # sin ruido en stdout
        pass

    def _send(self, code: int, body: bytes, content_type: str = "text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, location: str):
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/":
            query = parse_qs(url.query)
            m = manifest_mod.load(self.settings.manifest_path)
            items = gallery.collect_items(self.settings, m, self.slugs)
            page = render_page(self.settings, m, items, dict(self.jobs),
                               banner=query.get("ok", [""])[0] and
                               f"{query['ok'][0]} promocionado ✓",
                               error=query.get("err", [""])[0])
            self._send(200, page.encode())
            return
        if url.path == "/img":
            rel = parse_qs(url.query).get("p", [""])[0]
            target = (self.settings.repo_root / rel).resolve()
            if (self.settings.repo_root.resolve() not in target.parents
                    or target.suffix != ".png" or not target.is_file()):
                self._send(404, b"not found", "text/plain")
                return
            self._send(200, target.read_bytes(), "image/png")
            return
        self._send(404, b"not found", "text/plain")

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(length).decode("utf-8", errors="replace"))
        slug = form.get("slug", [""])[0]
        if path == "/promote":
            self._promote(slug, form.get("candidate", [""])[0])
        elif path == "/generate":
            self._more(slug)
        else:
            self._send(404, b"not found", "text/plain")

    def _promote(self, slug: str, candidate: str):
        target = (self.settings.repo_root / candidate).resolve()
        if self.settings.repo_root.resolve() not in target.parents or target.suffix != ".png":
            self._redirect("/?err=candidato+invalido")
            return
        try:
            m = manifest_mod.load(self.settings.manifest_path)
            promote_mod.promote(self.settings, m, slug, target)
            self._redirect(f"/?ok={slug}")
        except Exception as exc:
            traceback.print_exc()
            self._redirect(f"/?err={html.escape(str(exc)[:120])}")

    def _more(self, slug: str):
        if self.jobs.get(slug) == "running":
            self._redirect("/?err=ya+hay+una+generacion+en+curso")
            return
        self.jobs[slug] = "running"

        def job():
            try:
                _generate_more(self.settings, slug)
                self.jobs.pop(slug, None)
            except Exception as exc:
                self.jobs[slug] = f"ERROR: {str(exc)[:150]}"

        threading.Thread(target=job, daemon=True).start()
        self._redirect("/")


def make_server(settings: Settings, slugs: list[str] | None = None,
                port: int = 8765, host: str = "0.0.0.0") -> ThreadingHTTPServer:
    handler = type("BoundHandler", (ReviewHandler,),
                   {"settings": settings, "slugs": slugs, "jobs": {}})
    return ThreadingHTTPServer((host, port), handler)


def _lan_ip() -> str:
    import socket

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
            probe.connect(("8.8.8.8", 80))
            return probe.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def serve(settings: Settings, slugs: list[str] | None = None, port: int = 8765,
          host: str = "0.0.0.0") -> int:
    server = make_server(settings, slugs, port, host)
    real_port = server.server_address[1]
    shown = _lan_ip() if host == "0.0.0.0" else host
    print(f"revisión en http://{shown}:{real_port}/  (Ctrl-C para salir)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nadiós")
    finally:
        server.server_close()
    return 0
