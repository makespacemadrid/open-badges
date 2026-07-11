"""Carga/guardado del manifiesto badges.yaml (fuente de verdad local)."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from badgegen import config

DEFAULT_STYLE = (
    "Circular maker badge emblem, flat vector style, golden yellow (#F5C400) artwork "
    "on a black disc, outer yellow ring with small screw heads, bold sans-serif lettering, "
    "high contrast, clean centered composition, no gradients, no photo textures"
)
DEFAULT_REFERENCES = ["badge-template.png", "badge-member.png", "badge-hello-glados.png"]

STATUSES = ("ok", "missing", "regen")


@dataclass
class Badge:
    slug: str
    name: str
    file: str
    category: str = ""            # categorySlug del portal (presentación/docs)
    track: str | None = None      # escalera real de progresión (trackSlug)
    track_level: int | None = None
    description: str = ""
    criteria: str = ""
    visual: str | None = None
    status: str = "missing"
    issues: list[str] = field(default_factory=list)
    provider: str | None = None
    prompt_extra: str | None = None
    references: list[str] | None = None  # override por badge de reference_images (series)

    def to_dict(self) -> dict:
        d = {
            "slug": self.slug,
            "name": self.name,
            "file": self.file,
            "category": self.category,
            "description": self.description,
            "criteria": self.criteria,
            "status": self.status,
            "issues": list(self.issues),
        }
        for key in ("track", "track_level", "visual", "provider", "prompt_extra", "references"):
            value = getattr(self, key)
            if value is not None:
                d[key] = value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Badge":
        # compat: en manifiestos antiguos "track" contenía la categoría
        category = d.get("category")
        track = d.get("track")
        if category is None and isinstance(track, str) and track:
            category, track = track, None
        return cls(
            slug=d["slug"],
            name=d.get("name", d["slug"]),
            file=d.get("file", f"{d['slug']}.png"),
            category=category or "",
            track=track or None,
            track_level=d.get("track_level"),
            description=d.get("description", ""),
            criteria=d.get("criteria", ""),
            visual=d.get("visual"),
            status=d.get("status", "missing"),
            issues=list(d.get("issues") or []),
            provider=d.get("provider"),
            prompt_extra=d.get("prompt_extra"),
            references=list(d["references"]) if d.get("references") is not None else None,
        )


@dataclass
class Manifest:
    style: str = DEFAULT_STYLE
    reference_images: list[str] = field(default_factory=lambda: list(DEFAULT_REFERENCES))
    target_diameter: int = config.TARGET_DIAMETER
    roundness_threshold: float = config.ROUNDNESS_THRESHOLD
    badges: list[Badge] = field(default_factory=list)

    def get(self, slug: str) -> Badge | None:
        for badge in self.badges:
            if badge.slug == slug:
                return badge
        return None


def load(path: Path) -> Manifest:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return Manifest(
        style=data.get("style", DEFAULT_STYLE),
        reference_images=list(data.get("reference_images") or DEFAULT_REFERENCES),
        target_diameter=int(data.get("target_diameter", config.TARGET_DIAMETER)),
        roundness_threshold=float(data.get("roundness_threshold", config.ROUNDNESS_THRESHOLD)),
        badges=[Badge.from_dict(b) for b in data.get("badges") or []],
    )


def save(m: Manifest, path: Path) -> None:
    data = {
        "style": m.style,
        "reference_images": list(m.reference_images),
        "target_diameter": m.target_diameter,
        "roundness_threshold": m.roundness_threshold,
        "badges": [b.to_dict() for b in m.badges],
    }
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    path.write_text(text, encoding="utf-8")
