"""Gestor web de badges: revisión, generación, promoción y mantenimiento.

Solo stdlib. Pensado para migrar al portal de miembros: toda operación de la
UI pasa por un endpoint HTTP documentado (ver tools/README.md), y GET
/api/state expone el estado completo en JSON como contrato de integración.
"""
from __future__ import annotations

import html
import json
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlparse

from badgegen import catalog as catalog_mod, docs_gen, gallery, manifest as manifest_mod, promote as promote_mod
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
button.mini{background:#222;color:#bbb;border:1px solid #444;border-radius:5px;
  padding:.15rem .5rem;font-size:.8em;margin-left:.4rem}
select{background:#222;color:#eee;border:1px solid #444;border-radius:5px;padding:.2rem}
.dash{background:#1a1a1a;border-radius:8px;padding:.8rem 1rem;margin-bottom:1rem}
.dash .stat{margin-right:1.2rem}
.dash .stat b{color:#f5c400}
details{margin-top:1rem}
details>summary{cursor:pointer;background:#1a1a1a;padding:.6rem 1rem;border-radius:8px;
  font-size:1.1rem;font-weight:bold}
.context{margin:.3rem 0 1rem}
.context img{width:64px;height:64px;object-fit:contain;margin-right:.35rem;vertical-align:middle}
.context .lbl{color:#888;font-size:.85em;margin-right:.6rem}
.jobs{color:#f5c400}
.badge-name{color:#aaa;font-weight:normal}
.cand img{width:180px;height:180px;object-fit:contain}
.lvl{margin:.35rem 0;padding:.3rem .6rem;border-left:3px solid #333;border-radius:4px}
.lvl.done{border-color:#1c5c2e}
.lvl.pend{border-color:#f5c400;background:#181405}
.lvl img{width:72px;height:72px;object-fit:contain;vertical-align:middle;margin-right:.6rem}
.lvl .num{display:inline-block;min-width:3.2em;color:#f5c400;font-weight:bold}
.hint{color:#888;font-size:.85em}
.desc{color:#999;font-size:.85em;margin:.15rem 0 .35rem 3.8em}
textarea{background:#161616;color:#eee;border:1px solid #444;border-radius:6px;
  width:min(46rem,90%);padding:.4rem;font-family:inherit;font-size:.85em}
details.cfg{margin:.2rem 0 .6rem;font-size:.9em}
details.cfg>summary{background:none;padding:.1rem .3rem;font-size:.9em;
  font-weight:normal;color:#888}
details.cfg label{display:block;color:#888;font-size:.85em;margin-top:.4rem}
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

SCAN_JOB = "__scan__"
PROVIDERS = ("", "gemini", "custom")


# ─── operaciones (contrato para la migración al portal) ─────────────────────

def _generate_more(settings: Settings, slug: str, provider_name: str | None = None) -> None:
    """Genera 3 candidatos más para un badge (corre en un hilo)."""
    from badgegen import generate as generate_mod
    from badgegen.providers import get_provider

    m = manifest_mod.load(settings.manifest_path)
    badge = m.get(slug)
    if badge is None:
        raise KeyError(f"slug desconocido: {slug}")
    provider = get_provider(provider_name or badge.provider)
    report = generate_mod.run_generate(settings, m, provider, slugs=[slug], n=3)
    outcome = report.get(slug)
    if isinstance(outcome, str):
        raise RuntimeError(outcome)


def _run_scan(settings: Settings) -> None:
    """QC geométrico de todos los PNG finales; vuelca issues al manifiesto."""
    from PIL import Image

    from badgegen import qc

    m = manifest_mod.load(settings.manifest_path)
    for badge in m.badges:
        path = settings.repo_root / badge.file
        if badge.status != "ok" or not path.is_file():
            continue
        badge.issues = list(qc.check_image(Image.open(path),
                                           threshold=m.roundness_threshold).issues)
    manifest_mod.save(m, settings.manifest_path)


def _run_sync(settings: Settings) -> str:
    m = (manifest_mod.load(settings.manifest_path)
         if settings.manifest_path.is_file() else manifest_mod.Manifest())
    entries = catalog_mod.parse_catalog(settings.catalog_path)
    warnings = catalog_mod.merge_catalog(m, entries, settings.repo_root)
    manifest_mod.save(m, settings.manifest_path)
    counts = {s: sum(1 for b in m.badges if b.status == s) for s in ("ok", "missing", "regen")}
    extra = f" · {len(warnings)} avisos" if warnings else ""
    return f"sync: {len(m.badges)} badges ({counts['ok']} ok, {counts['missing']} missing){extra}"


def _run_fix(settings: Settings, slug: str) -> None:
    m = manifest_mod.load(settings.manifest_path)
    promote_mod.fix(settings, m, slug)


def _edit_badge(settings: Settings, slug: str, visual: str, prompt_extra: str,
                references: str) -> None:
    m = manifest_mod.load(settings.manifest_path)
    badge = m.get(slug)
    if badge is None:
        raise KeyError(f"slug desconocido: {slug}")
    badge.visual = visual.strip() or None
    badge.prompt_extra = prompt_extra.strip() or None
    refs = [line.strip() for line in references.splitlines() if line.strip()]
    badge.references = refs or None
    manifest_mod.save(m, settings.manifest_path)


def _edit_track(settings: Settings, track: str, references: str, prompt_extra: str) -> None:
    m = manifest_mod.load(settings.manifest_path)
    refs = [line.strip() for line in references.splitlines() if line.strip()]
    cfg = manifest_mod.TrackConfig(references=refs,
                                   prompt_extra=prompt_extra.strip() or None)
    if cfg.empty:
        m.tracks.pop(track, None)
    else:
        m.tracks[track] = cfg
    manifest_mod.save(m, settings.manifest_path)


def _edit_globals(settings: Settings, style: str, references: str) -> None:
    m = manifest_mod.load(settings.manifest_path)
    if style.strip():
        m.style = style.strip()
    refs = [line.strip() for line in references.splitlines() if line.strip()]
    if refs:
        m.reference_images = refs
    manifest_mod.save(m, settings.manifest_path)


def api_state(settings: Settings, m, jobs: dict[str, str]) -> dict:
    items = {i["slug"]: i for i in gallery.collect_items(settings, m)}
    badges = []
    for b in m.badges:
        d = b.to_dict()
        d["has_image"] = (settings.repo_root / b.file).is_file()
        d["candidates"] = items.get(b.slug, {}).get("candidates", [])
        badges.append(d)
    return {
        "badges": badges,
        "jobs": dict(jobs),
        "counts": {s: sum(1 for b in m.badges if b.status == s)
                   for s in ("ok", "missing", "regen")},
        "style": m.style,
        "reference_images": list(m.reference_images),
        "tracks": {slug: cfg.to_dict() for slug, cfg in m.tracks.items()},
        "target_diameter": m.target_diameter,
    }


# ─── render ──────────────────────────────────────────────────────────────────

def _provider_select(slug: str) -> str:
    options = "".join(
        f"<option value='{p}'>{p or 'auto'}</option>" for p in PROVIDERS
    )
    return (f"<form method='post' action='/generate'>"
            f"<input type='hidden' name='slug' value='{html.escape(slug)}'>"
            f"<select name='provider'>{options}</select> ")


def render_page(settings: Settings, m, items: list[dict], jobs: dict[str, str],
                banner: str = "", error: str = "") -> str:
    items_by_slug = {i["slug"]: i for i in items}
    parts = []
    refreshing = any(status == "running" for status in jobs.values())
    if banner:
        parts.append(f"<div class='banner'>{html.escape(banner)}</div>")
    if error:
        parts.append(f"<div class='banner err'>{html.escape(error)}</div>")

    parts.append(_render_dashboard(m, items, jobs))

    # 1. Tracks: cada escalera completa, nivel a nivel, con acciones inline.
    all_tracks = sorted({b.track for b in m.badges if b.track},
                        key=lambda t: TRACK_TITLES.get(t, t))
    for track in all_tracks:
        parts.append(_render_track(settings, m, track, items_by_slug, jobs))

    # 2. Badges sin track, por categoría (catálogo completo, colapsable).
    trackless = [b for b in m.badges if not b.track]
    by_cat: dict[str, list] = {}
    for badge in trackless:
        by_cat.setdefault(badge.category, []).append(badge)
    for category in sorted(by_cat, key=lambda c: _CATEGORY_NAMES.get(c, c)):
        badges = by_cat[category]
        pending = [b for b in badges if b.status != "ok" or b.slug in items_by_slug]
        title = _CATEGORY_NAMES.get(category, category or "Otros")
        done = sum(1 for b in badges if b.status == "ok")
        state = " open" if pending else ""
        parts.append(f"<details{state}><summary>{html.escape(title)} "
                     f"<span class='badge-name'>— {done}/{len(badges)} con imagen"
                     f"{' · ' + str(len(pending)) + ' pendientes' if pending else ''}"
                     f"</span></summary>")
        for badge in sorted(badges, key=lambda b: (b.status == "ok", b.slug)):
            parts.append(_render_row(settings, badge, items_by_slug.get(badge.slug),
                                     jobs, level_label=""))
        parts.append("</details>")

    refresh = "<meta http-equiv='refresh' content='8'>" if refreshing else ""
    return (
        f"<!doctype html><html><head><meta charset='utf-8'>{refresh}"
        f"<title>badgegen · gestor</title><style>{_SERVE_CSS}</style></head>"
        f"<body><h1>badgegen · gestor de badges</h1>{''.join(parts)}</body></html>"
    )


def _render_dashboard(m, items: list[dict], jobs: dict[str, str]) -> str:
    counts = {s: sum(1 for b in m.badges if b.status == s) for s in ("ok", "missing", "regen")}
    n_candidates = sum(len(i["candidates"]) for i in items)
    with_issues = sum(1 for b in m.badges if b.issues)
    scan_status = jobs.get(SCAN_JOB, "")
    scan_note = " ⏳" if scan_status == "running" else ""
    parts = [
        "<div class='dash'>",
        f"<span class='stat'><b>{counts['ok']}</b> con imagen</span>",
        f"<span class='stat'><b>{counts['missing']}</b> pendientes</span>",
        f"<span class='stat'><b>{counts['regen']}</b> a regenerar</span>",
        f"<span class='stat'><b>{n_candidates}</b> candidatos por revisar</span>",
        f"<span class='stat'><b>{with_issues}</b> con issues de QC</span> · ",
        "<form method='post' action='/sync'><button class='more'>Sync catálogo</button></form> ",
        f"<form method='post' action='/scan'><button class='more'>Scan QC{scan_note}</button></form> ",
        "<form method='post' action='/docs'><button class='more'>Regenerar docs</button></form>",
    ]
    if scan_status.startswith("ERROR"):
        parts.append(f"<div class='banner err'>scan: {html.escape(scan_status)}</div>")
    parts.append(
        "<details class='cfg'><summary>⚙ configuración global (estilo y referencias)</summary>"
        "<form method='post' action='/globals'>"
        "<label>Prompt de estilo global</label>"
        f"<textarea name='style' rows='3'>{html.escape(m.style)}</textarea>"
        "<label>Badges/artworks de referencia globales (uno por línea)</label>"
        f"<textarea name='references' rows='3'>"
        f"{html.escape(chr(10).join(m.reference_images))}</textarea><br>"
        "<button class='mini'>Guardar</button></form></details>"
    )
    parts.append("</div>")
    return "".join(parts)


def _render_track(settings: Settings, m, track: str, items_by_slug: dict,
                  jobs: dict[str, str]) -> str:
    members = sorted((b for b in m.badges if b.track == track),
                     key=lambda b: (b.track_level or 0, b.slug))
    done = sum(1 for b in members if b.status == "ok")
    pending = [b for b in members if b.status != "ok" or b.slug in items_by_slug]
    title = TRACK_TITLES.get(track, track)
    state = " open" if pending else ""
    parts = [f"<details{state}><summary>{html.escape(title)} "
             f"<span class='badge-name'>— {done}/{len(members)} con imagen"
             f"{' · ' + str(len(pending)) + ' pendientes' if pending else ''}"
             f"</span></summary>"]
    parts.append(_render_track_config(settings, m, track))
    for badge in members:
        label = f"lvl {badge.track_level}" if badge.track_level is not None else "—"
        parts.append(_render_row(settings, badge, items_by_slug.get(badge.slug),
                                 jobs, level_label=label))
    parts.append("</details>")
    return "".join(parts)


def _render_track_config(settings: Settings, m, track: str) -> str:
    cfg = m.tracks.get(track) or manifest_mod.TrackConfig()
    thumbs = "".join(
        f"<img src='/img?p={html.escape(r)}' title='{html.escape(r)}'>"
        for r in cfg.references if (settings.repo_root / r).is_file()
    )
    return (
        f"<details class='cfg'><summary>⚙ configurar track "
        f"(artworks y prompt de la serie)</summary>"
        f"{f'<div class=context>{thumbs}</div>' if thumbs else ''}"
        f"<form method='post' action='/track'>"
        f"<input type='hidden' name='track' value='{html.escape(track)}'>"
        f"<label>Artworks/badges de referencia del track (uno por línea, "
        f"se SUMAN a los del badge; p.ej. assets/makespace-icon.png)</label>"
        f"<textarea name='references' rows='2'>"
        f"{html.escape(chr(10).join(cfg.references))}</textarea>"
        f"<label>Prompt común del track (se añade a todos sus badges)</label>"
        f"<textarea name='prompt_extra' rows='2'>"
        f"{html.escape(cfg.prompt_extra or '')}</textarea><br>"
        f"<button class='mini'>Guardar track</button></form></details>"
    )


def _render_edit_form(badge) -> str:
    refs = "\n".join(badge.references or [])
    return (
        f"<details class='cfg'><summary>✏ editar prompt/referencias</summary>"
        f"<form method='post' action='/edit'>"
        f"<input type='hidden' name='slug' value='{html.escape(badge.slug)}'>"
        f"<label>Motivo visual (visual)</label>"
        f"<textarea name='visual' rows='2'>{html.escape(badge.visual or '')}</textarea>"
        f"<label>Prompt extra del badge</label>"
        f"<textarea name='prompt_extra' rows='2'>{html.escape(badge.prompt_extra or '')}</textarea>"
        f"<label>Referencias propias (una por línea; sustituyen a las globales)</label>"
        f"<textarea name='references' rows='2'>{html.escape(refs)}</textarea><br>"
        f"<button class='mini'>Guardar</button></form></details>"
    )


def _render_row(settings: Settings, badge, item: dict | None,
                jobs: dict[str, str], level_label: str) -> str:
    """Una fila por badge: imagen y acciones si existe; candidatos o generar si no."""
    num = f"<span class='num'>{html.escape(level_label)}</span>" if level_label else ""
    name = html.escape(badge.name)
    slug = html.escape(badge.slug)
    status = jobs.get(badge.slug, "")
    issues = "".join(f"<span class='issue'>{html.escape(i)}</span>" for i in badge.issues)

    if badge.status == "ok" and (settings.repo_root / badge.file).is_file() and not item:
        row = (f"<div class='lvl done'><img src='/img?p={html.escape(badge.file)}'>"
               f"{num} {name} <span class='badge-name'>✓</span> {issues}")
        if status == "running":
            return row + " <span class='jobs'>⏳ generando…</span></div>"
        if status.startswith("ERROR"):
            row += f" <span class='issue'>{html.escape(status)}</span>"
        row += (f" {_provider_select(badge.slug)}"
                f"<button class='mini'>Regenerar</button></form>"
                f"<form method='post' action='/fix'>"
                f"<input type='hidden' name='slug' value='{slug}'>"
                f"<button class='mini'>Fix círculo</button></form>")
        return row + "</div>" + _render_edit_form(badge)

    parts = [f"<div class='lvl pend'>{num} <b>{name}</b> "
             f"<span class='badge-name'><code>{slug}</code></span> {issues}"]
    if status == "running":
        parts.append(" <span class='jobs'>⏳ generando…</span></div>")
        return "".join(parts)
    if status.startswith("ERROR"):
        parts.append(f" <span class='issue'>{html.escape(status)}</span>")
    parts.append("</div>")
    detail = badge.visual or badge.description
    if detail:
        parts.append(f"<div class='desc'>{html.escape(detail)}</div>")
    parts.append(_render_edit_form(badge))

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
        parts.append(f"<div class='cand'>{_provider_select(badge.slug)}"
                     f"<button class='more'>＋3 sugerencias</button></form></div>")
    else:
        hint = ""
        if badge.references and not any(
            (settings.repo_root / r).is_file() for r in badge.references
        ):
            hint = (" <span class='hint'>⚠ su nivel anterior aún no tiene imagen; "
                    "usará las referencias globales</span>")
        parts.append(f"<div class='cand'>{_provider_select(badge.slug)}"
                     f"<button class='more'>Generar 3 candidatos</button></form>{hint}</div>")
    return "".join(parts)


# ─── HTTP ────────────────────────────────────────────────────────────────────

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
                               banner=query.get("ok", [""])[0],
                               error=query.get("err", [""])[0])
            self._send(200, page.encode())
            return
        if url.path == "/api/state":
            m = manifest_mod.load(self.settings.manifest_path)
            body = json.dumps(api_state(self.settings, m, self.jobs),
                              ensure_ascii=False).encode()
            self._send(200, body, "application/json; charset=utf-8")
            return
        if url.path == "/img":
            rel = parse_qs(url.query).get("p", [""])[0]
            target = (self.settings.repo_root / rel).resolve()
            if (self.settings.repo_root.resolve() not in target.parents
                    or target.suffix != ".png" or not target.is_file()):
                self._send(404, b"not found", "text/plain")
                return
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Cache-Control", "max-age=30")
            body = target.read_bytes()
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
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
            self._more(slug, form.get("provider", [""])[0] or None)
        elif path == "/fix":
            self._sync_op(lambda: _run_fix(self.settings, slug),
                          ok=f"{slug} circularizado ✓")
        elif path == "/sync":
            self._sync_op(lambda: _run_sync(self.settings), use_result=True)
        elif path == "/docs":
            self._sync_op(lambda: docs_gen.write_docs(
                self.settings, manifest_mod.load(self.settings.manifest_path)),
                ok="README y missing-images regenerados ✓")
        elif path == "/scan":
            self._scan()
        elif path == "/edit":
            self._sync_op(lambda: _edit_badge(
                self.settings, slug,
                form.get("visual", [""])[0],
                form.get("prompt_extra", [""])[0],
                form.get("references", [""])[0]),
                ok=f"{slug} actualizado ✓")
        elif path == "/track":
            track = form.get("track", [""])[0]
            self._sync_op(lambda: _edit_track(
                self.settings, track,
                form.get("references", [""])[0],
                form.get("prompt_extra", [""])[0]),
                ok=f"track {track} actualizado ✓")
        elif path == "/globals":
            self._sync_op(lambda: _edit_globals(
                self.settings,
                form.get("style", [""])[0],
                form.get("references", [""])[0]),
                ok="configuración global guardada ✓")
        else:
            self._send(404, b"not found", "text/plain")

    def _sync_op(self, fn, ok: str = "hecho ✓", use_result: bool = False):
        try:
            result = fn()
            self._redirect(f"/?ok={quote(str(result if use_result else ok))}")
        except Exception as exc:
            traceback.print_exc()
            self._redirect(f"/?err={quote(str(exc)[:120])}")

    def _promote(self, slug: str, candidate: str):
        target = (self.settings.repo_root / candidate).resolve()
        if self.settings.repo_root.resolve() not in target.parents or target.suffix != ".png":
            self._redirect("/?err=candidato+invalido")
            return
        try:
            m = manifest_mod.load(self.settings.manifest_path)
            promote_mod.promote(self.settings, m, slug, target)
            self._redirect(f"/?ok={quote(f'{slug} promocionado ✓')}")
        except Exception as exc:
            traceback.print_exc()
            self._redirect(f"/?err={quote(str(exc)[:120])}")

    def _more(self, slug: str, provider: str | None):
        if provider not in (None, "gemini", "custom"):
            self._redirect("/?err=proveedor+invalido")
            return
        if self.jobs.get(slug) == "running":
            self._redirect("/?err=ya+hay+una+generacion+en+curso")
            return
        self.jobs[slug] = "running"

        def job():
            try:
                _generate_more(self.settings, slug, provider)
                self.jobs.pop(slug, None)
            except Exception as exc:
                self.jobs[slug] = f"ERROR: {str(exc)[:150]}"

        threading.Thread(target=job, daemon=True).start()
        self._redirect("/")

    def _scan(self):
        if self.jobs.get(SCAN_JOB) == "running":
            self._redirect("/?err=scan+en+curso")
            return
        self.jobs[SCAN_JOB] = "running"

        def job():
            try:
                _run_scan(self.settings)
                self.jobs.pop(SCAN_JOB, None)
            except Exception as exc:
                self.jobs[SCAN_JOB] = f"ERROR: {str(exc)[:150]}"

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
    print(f"gestor en http://{shown}:{real_port}/  (Ctrl-C para salir)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nadiós")
    finally:
        server.server_close()
    return 0
