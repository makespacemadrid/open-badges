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
.context img{width:64px;height:64px;object-fit:contain;margin-right:.35rem;vertical-align:middle}
.context .lbl{color:#888;font-size:.85em;margin-right:.6rem}
h3{margin-bottom:.2rem}
.jobs{color:#f5c400}
.badge-name{color:#aaa;font-weight:normal}
.cand img{width:180px;height:180px;object-fit:contain}
.lvl{margin:.35rem 0;padding:.3rem .6rem;border-left:3px solid #333;border-radius:4px}
.lvl.done{border-color:#1c5c2e}
.lvl.pend{border-color:#f5c400;background:#181405}
.lvl img{width:72px;height:72px;object-fit:contain;vertical-align:middle;margin-right:.6rem}
.lvl .num{display:inline-block;min-width:3.2em;color:#f5c400;font-weight:bold}
.hint{color:#888;font-size:.85em}
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


def render_page(settings: Settings, m, items: list[dict], jobs: dict[str, str],
                banner: str = "", error: str = "") -> str:
    items_by_slug = {i["slug"]: i for i in items}
    parts = []
    refreshing = any(status == "running" for status in jobs.values())
    if banner:
        parts.append(f"<div class='banner'>{html.escape(banner)}</div>")
    if error:
        parts.append(f"<div class='banner err'>{html.escape(error)}</div>")
    missing_total = sum(1 for b in m.badges if b.status != "ok")
    if not items and not missing_total and not refreshing:
        parts.append("<p>Catálogo completo: nada pendiente. 🎉</p>")

    # 1. Tracks: cada escalera completa, nivel a nivel, con acciones inline.
    all_tracks = sorted({b.track for b in m.badges if b.track},
                        key=lambda t: TRACK_TITLES.get(t, t))
    for track in all_tracks:
        parts.append(_render_track(settings, m, track, items_by_slug, jobs))

    # 2. Badges sin track, por categoría: solo categorías con trabajo pendiente.
    trackless = [b for b in m.badges if not b.track]
    by_cat: dict[str, list] = {}
    for badge in trackless:
        by_cat.setdefault(badge.category, []).append(badge)
    for category in sorted(by_cat, key=lambda c: _CATEGORY_NAMES.get(c, c)):
        badges = by_cat[category]
        pending = [b for b in badges if b.status != "ok" or b.slug in items_by_slug]
        if not pending:
            continue
        title = _CATEGORY_NAMES.get(category, category or "Otros")
        parts.append(f"<h2 class='track'>{html.escape(title)}</h2>")
        existing = [b for b in badges if b.status == "ok"
                    and (settings.repo_root / b.file).is_file()]
        if existing:
            thumbs = "".join(
                f"<img src='/img?p={html.escape(b.file)}' title='{html.escape(b.name)}'>"
                for b in existing
            )
            parts.append(f"<div class='context'><span class='lbl'>ya en la categoría "
                         f"({len(existing)}):</span>{thumbs}</div>")
        for badge in pending:
            parts.append(_render_row(settings, badge, items_by_slug.get(badge.slug),
                                     jobs, level_label=""))

    refresh = "<meta http-equiv='refresh' content='8'>" if refreshing else ""
    return (
        f"<!doctype html><html><head><meta charset='utf-8'>{refresh}"
        f"<title>badgegen · revisión</title><style>{_SERVE_CSS}</style></head>"
        f"<body><h1>badgegen · revisión de candidatos</h1>{''.join(parts)}</body></html>"
    )


def _render_track(settings: Settings, m, track: str, items_by_slug: dict,
                  jobs: dict[str, str]) -> str:
    members = sorted((b for b in m.badges if b.track == track),
                     key=lambda b: (b.track_level or 0, b.slug))
    done = sum(1 for b in members if b.status == "ok")
    title = TRACK_TITLES.get(track, track)
    parts = [f"<h2 class='track'>{html.escape(title)} "
             f"<span class='badge-name'>— {done}/{len(members)} con imagen</span></h2>"]
    for badge in members:
        label = f"lvl {badge.track_level}" if badge.track_level is not None else "—"
        parts.append(_render_row(settings, badge, items_by_slug.get(badge.slug),
                                 jobs, level_label=label))
    return "".join(parts)


def _render_row(settings: Settings, badge, item: dict | None,
                jobs: dict[str, str], level_label: str) -> str:
    """Una fila por badge: imagen si existe, candidatos si los hay, o generar."""
    num = f"<span class='num'>{html.escape(level_label)}</span>" if level_label else ""
    name = html.escape(badge.name)
    slug = html.escape(badge.slug)
    status = jobs.get(badge.slug, "")

    if badge.status == "ok" and (settings.repo_root / badge.file).is_file() and not item:
        return (f"<div class='lvl done'><img src='/img?p={html.escape(badge.file)}'>"
                f"{num} {name} <span class='badge-name'>✓</span></div>")

    parts = [f"<div class='lvl pend'>{num} <b>{name}</b> "
             f"<span class='badge-name'><code>{slug}</code></span>"]
    if status == "running":
        parts.append(" <span class='jobs'>⏳ generando…</span></div>")
        return "".join(parts)
    if status.startswith("ERROR"):
        parts.append(f" <span class='issue'>{html.escape(status)}</span>")
    parts.append("</div>")

    if item:
        if item.get("current"):
            parts.append(
                f"<div class='cand'><img src='/img?p={html.escape(item['current'])}'>"
                f"<div>actual</div></div>"
            )
        for cand in item["candidates"]:
            qc_class = "good" if cand["qc_ok"] else "bad"
            qc_label = "QC ok" if cand["qc_ok"] else "QC ✗"
            parts.append(
                f"<div class='cand'><img src='/img?p={html.escape(cand['file'])}'>"
                f"<div><span class='qc {qc_class}'>{qc_label}</span> {cand['roundness']:.3f} "
                f"· {html.escape(cand['provider'])}</div>"
                f"<form method='post' action='/promote'>"
                f"<input type='hidden' name='slug' value='{slug}'>"
                f"<input type='hidden' name='candidate' value='{html.escape(cand['file'])}'>"
                f"<button class='promote'>Promocionar ✓</button></form></div>"
            )
        parts.append(
            f"<div class='cand'><form method='post' action='/generate'>"
            f"<input type='hidden' name='slug' value='{slug}'>"
            f"<button class='more'>＋3 sugerencias</button></form></div>"
        )
    else:
        hint = ""
        if badge.references and not any(
            (settings.repo_root / r).is_file() for r in badge.references
        ):
            hint = (" <span class='hint'>⚠ su nivel anterior aún no tiene imagen; "
                    "usará las referencias globales</span>")
        parts.append(
            f"<div class='cand'><form method='post' action='/generate'>"
            f"<input type='hidden' name='slug' value='{slug}'>"
            f"<button class='more'>Generar 3 candidatos</button></form>{hint}</div>"
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
