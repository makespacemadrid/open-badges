"""Servidor local de revisión: galería con botón Promocionar, sin copy-paste.

Solo stdlib. Escucha en 127.0.0.1; cada POST /promote ejecuta el promote
completo (post-proceso, manifiesto, purge, docs) y la página se refresca.
"""
from __future__ import annotations

import html
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from badgegen import gallery, manifest as manifest_mod, promote as promote_mod
from badgegen.config import Settings

_SERVE_CSS = gallery._CSS + """
.banner{background:#1c5c2e;padding:.5rem 1rem;border-radius:8px;margin-bottom:1rem}
.banner.err{background:#7a2020}
form{display:inline}
button.promote{background:#f5c400;color:#111;font-weight:bold;border:0;
  border-radius:6px;padding:.4rem .8rem}
"""


def render_page(items: list[dict], banner: str = "", error: str = "") -> str:
    parts = []
    if banner:
        parts.append(f"<div class='banner'>{html.escape(banner)}</div>")
    if error:
        parts.append(f"<div class='banner err'>{html.escape(error)}</div>")
    if not items:
        parts.append("<p>No quedan candidatos pendientes. 🎉</p>")
    for item in items:
        parts.append(f"<h2><code>{html.escape(item['slug'])}</code></h2>")
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
                f"<input type='hidden' name='slug' value='{html.escape(item['slug'])}'>"
                f"<input type='hidden' name='candidate' value='{html.escape(cand['file'])}'>"
                f"<button class='promote'>Promocionar ✓</button></form></div>"
            )
    body = "".join(parts)
    return (
        f"<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>badgegen · revisión</title><style>{_SERVE_CSS}</style></head>"
        f"<body><h1>badgegen · revisión de candidatos</h1>{body}</body></html>"
    )


class ReviewHandler(BaseHTTPRequestHandler):
    # inyectados por make_server en la clase derivada:
    settings: Settings
    slugs: list[str] | None

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
            page = render_page(items,
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
        if urlparse(self.path).path != "/promote":
            self._send(404, b"not found", "text/plain")
            return
        length = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.body_text(length))
        slug = form.get("slug", [""])[0]
        candidate = form.get("candidate", [""])[0]
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

    def body_text(self, length: int) -> str:
        return self.rfile.read(length).decode("utf-8", errors="replace")


def make_server(settings: Settings, slugs: list[str] | None = None,
                port: int = 8765, host: str = "0.0.0.0") -> ThreadingHTTPServer:
    handler = type("BoundHandler", (ReviewHandler,),
                   {"settings": settings, "slugs": slugs})
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
    print(f"revisión en http://{shown}:{real_port}/  (Ctrl-C para salir)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nadiós")
    finally:
        server.server_close()
    return 0
