"""Orquestación de la generación de candidatos."""
from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

from badgegen import qc
from badgegen.config import Settings
from badgegen.manifest import Badge, Manifest

HARD_RULES = (
    "Hard requirements: the badge is a PERFECT CIRCLE (never an ellipse or squashed disc), "
    "fully visible and centered with margin around it, on a plain solid black background with "
    "nothing else in the frame. Any text must be spelled EXACTLY as given, fully legible, "
    "with clean unbroken letterforms. The title appears exactly ONCE, at the top of the badge."
)


def build_prompt(m: Manifest, b: Badge) -> str:
    motif = b.visual or b.description
    lines = [
        m.style.strip(),
        f'Badge title text (must appear exactly): "{b.name}"',
        f"Main motif: {motif}",
    ]
    track_cfg = m.track_config(b.track)
    if track_cfg and track_cfg.prompt_extra:
        lines.append(track_cfg.prompt_extra)
    if b.prompt_extra:
        lines.append(b.prompt_extra)
    lines.append(HARD_RULES)
    return "\n".join(lines)


def select_badges(m: Manifest, slugs: list[str] | None,
                  statuses: list[str] | None) -> list[Badge]:
    if slugs:
        result = []
        for slug in slugs:
            badge = m.get(slug)
            if badge is None:
                raise KeyError(f"slug desconocido: {slug}")
            result.append(badge)
        return result
    if statuses:
        return [b for b in m.badges if b.status in statuses]
    return []


def _next_index(directory: Path) -> int:
    existing = [int(p.name.split("-")[0]) for p in directory.glob("*.png")
                if p.name.split("-")[0].isdigit()]
    return max(existing, default=0) + 1


def _load_files(settings: Settings, names: list[str]) -> list[bytes]:
    return [
        (settings.repo_root / name).read_bytes()
        for name in names
        if (settings.repo_root / name).is_file()
    ]


def badge_references(settings: Settings, m: Manifest, badge: Badge) -> list[bytes]:
    """Referencias efectivas del badge.

    Base: las suyas (cadena de serie) o, si no tiene, las globales. A eso se
    SUMAN los artworks del track (p.ej. el icono de Makespace en antigüedad).
    Si nada de lo anterior existe en disco todavía, caen a las globales.
    """
    base = badge.references or m.reference_images
    track_cfg = m.track_config(badge.track)
    extra = track_cfg.references if track_cfg else []
    names = list(dict.fromkeys(list(base) + list(extra)))
    refs = _load_files(settings, names)
    if refs:
        return refs
    return _load_files(settings, m.reference_images)


def run_generate(settings: Settings, m: Manifest, provider,
                 slugs: list[str] | None = None, statuses: list[str] | None = None,
                 n: int = 4) -> dict:
    overrides: dict = {}
    report: dict = {}
    for badge in select_badges(m, slugs, statuses):
        try:
            badge_provider = provider
            if badge.provider and badge.provider != provider.name:
                if badge.provider not in overrides:
                    from badgegen.providers import get_provider

                    overrides[badge.provider] = get_provider(badge.provider)
                badge_provider = overrides[badge.provider]
            references = badge_references(settings, m, badge)
            report[badge.slug] = _generate_one(settings, m, badge_provider, badge, references, n)
        except Exception as exc:  # el batch sigue; el error queda en el informe
            report[badge.slug] = f"ERROR: {exc}"
    return report


def _generate_one(settings: Settings, m: Manifest, provider, badge: Badge,
                  references: list[bytes], n: int) -> list[str]:
    prompt = build_prompt(m, badge)
    directory = settings.candidates_dir / badge.slug
    directory.mkdir(parents=True, exist_ok=True)
    saved = []
    for image_bytes in provider.generate(prompt, references, n):
        index = _next_index(directory)
        stem = f"{index:02d}-{provider.name}"
        png_path = directory / f"{stem}.png"
        png_path.write_bytes(image_bytes)
        result = qc.check_image(Image.open(io.BytesIO(image_bytes)),
                                threshold=m.roundness_threshold)
        sidecar = {
            "slug": badge.slug,
            "prompt": prompt,
            "provider": provider.name,
            "model": provider.model,
            "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "qc": {"roundness": round(result.roundness, 4), "issues": result.issues},
        }
        (directory / f"{stem}.json").write_text(
            json.dumps(sidecar, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        saved.append(str(png_path.relative_to(settings.repo_root)))
    return saved
