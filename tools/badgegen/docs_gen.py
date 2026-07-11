"""Regeneración de las tablas de README.md y missing-images.md desde el manifiesto."""
from __future__ import annotations

import re

from badgegen.config import Settings
from badgegen.manifest import Badge, Manifest

START = "<!-- badgegen:tables:start -->"
END = "<!-- badgegen:tables:end -->"

TRACKS = [
    ("onboarding", "Onboarding"),
    ("maquinas", "Máquinas"),
    ("plataformas", "Plataformas"),
    ("comunidad", "Comunidad"),
    ("eventos", "Eventos"),
    ("membresia", "Membresía"),
]


class MarkersMissing(Exception):
    pass


def _by_track(badges: list[Badge]) -> list[tuple[str, list[Badge]]]:
    known = {slug for slug, _ in TRACKS}
    groups = []
    for slug, title in TRACKS:
        items = sorted((b for b in badges if b.track == slug), key=lambda b: b.slug)
        if items:
            groups.append((title, items))
    others = sorted((b for b in badges if b.track not in known), key=lambda b: b.slug)
    if others:
        groups.append(("Otros", others))
    return groups


def _estado(b: Badge) -> str:
    if b.status == "ok":
        return "✅"
    if b.status == "regen":
        return "🔄 regenerar"
    return "❌ pendiente"


def render_readme_tables(m: Manifest) -> str:
    total = len(m.badges)
    sin_imagen = sum(1 for b in m.badges if b.status == "missing")
    parts = [
        "## Catálogo de badges",
        "",
        f"_Generado por `badgegen docs` desde `badges.yaml` ({total} badges activos, "
        f"{sin_imagen} sin imagen)._",
    ]
    for title, items in _by_track(m.badges):
        parts += ["", f"### {title}", "", "| Slug | Nombre | Imagen | Estado |",
                  "|------|--------|--------|--------|"]
        parts += [f"| `{b.slug}` | {b.name} | `{b.file}` | {_estado(b)} |" for b in items]
    return "\n".join(parts)


def render_missing(m: Manifest) -> str:
    pending = [b for b in m.badges if b.status in ("missing", "regen")]
    parts = [
        f"Badges sin imagen o marcados para regenerar ({len(pending)}). "
        "Convención: `badge-<slug>.png`.",
        "",
        "Tras subir una imagen, purga la caché de jsDelivr: "
        "`https://purge.jsdelivr.net/gh/makespacemadrid/open-badges@main/<filename>`.",
    ]
    for title, items in _by_track(pending):
        parts += ["", f"## {title}", "", "| Slug | Nombre | Archivo | Estado |",
                  "|------|--------|---------|--------|"]
        parts += [f"| `{b.slug}` | {b.name} | `{b.file}` | {_estado(b)} |" for b in items]
    return "\n".join(parts)


def replace_between(text: str, content: str) -> str:
    if START not in text or END not in text:
        raise MarkersMissing(
            f"faltan los marcadores {START} / {END}; añádelos alrededor de las tablas"
        )
    pattern = re.compile(re.escape(START) + ".*?" + re.escape(END), re.DOTALL)
    return pattern.sub(f"{START}\n{content}\n{END}", text)


def write_docs(settings: Settings, m: Manifest) -> None:
    for path, content in (
        (settings.readme_path, render_readme_tables(m)),
        (settings.missing_path, render_missing(m)),
    ):
        path.write_text(
            replace_between(path.read_text(encoding="utf-8"), content), encoding="utf-8"
        )
