"""Parser del catálogo TypeScript del portal (const BADGES: BadgeSpec[]).

Extrae también los tracks reales: las quests llevan trackSlug/trackLevel y
los badges los heredan vía questSlugs; los badges "de colección" llevan su
propio trackSlug + trackCountThreshold. categorySlug es solo la categoría
de presentación.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


class CatalogParseError(Exception):
    pass


@dataclass
class CatalogEntry:
    slug: str
    name: str
    description: str
    criteria: str
    category: str
    image_file: str | None
    retired: bool
    track: str | None = None
    track_level: int | None = None


def default_file(slug: str) -> str:
    return f"{slug}.png" if slug.startswith("badge-") else f"badge-{slug}.png"


def _split_entries(text: str, array_name: str = "BADGES") -> list[str]:
    """Devuelve los literales {...} de primer nivel de un array const.

    Scanner de caracteres consciente de strings ('", `) con escapes, de
    comentarios // y /* */, y de anidamiento de llaves/corchetes: los regex
    no valen porque las entradas contienen questGroups: [{...}] anidados.
    """
    marker = re.search(rf"const\s+{array_name}\s*:[^=]*=\s*\[", text)
    if not marker:
        raise CatalogParseError(f"no se encontró 'const {array_name}' en el catálogo")
    i = marker.end()
    entries: list[str] = []
    depth_braces = 0
    depth_brackets = 1  # ya estamos dentro del [
    in_string: str | None = None
    start = None
    while i < len(text):
        ch = text[i]
        if in_string:
            if ch == "\\":
                i += 2
                continue
            if ch == in_string:
                in_string = None
        elif ch == "/" and text[i + 1 : i + 2] == "/":
            i = text.find("\n", i)
            if i == -1:
                break
            continue
        elif ch == "/" and text[i + 1 : i + 2] == "*":
            end = text.find("*/", i + 2)
            i = end + 2 if end != -1 else len(text)
            continue
        elif ch in ("'", '"', "`"):
            in_string = ch
        elif ch == "{":
            if depth_braces == 0 and depth_brackets == 1:
                start = i
            depth_braces += 1
        elif ch == "}":
            depth_braces -= 1
            if depth_braces == 0 and start is not None:
                entries.append(text[start : i + 1])
                start = None
        elif ch == "[":
            depth_brackets += 1
        elif ch == "]":
            depth_brackets -= 1
            if depth_brackets == 0:
                break
        i += 1
    if not entries:
        raise CatalogParseError(
            f"0 entradas en {array_name}: ¿cambió el formato del catálogo?"
        )
    return entries


_STRING = r"'((?:[^'\\]|\\.)*)'"
_STRING_DQ = r'"((?:[^"\\]|\\.)*)"'


def _field(chunk: str, key: str) -> str | None:
    for pattern, quote in ((_STRING, "'"), (_STRING_DQ, '"')):
        m = re.search(rf"(?<![A-Za-z]){key}:\s*{pattern}", chunk, re.DOTALL)
        if m:
            return m.group(1).replace("\\" + quote, quote).replace("\\\\", "\\")
    return None


def _quest_tracks(text: str) -> dict[str, tuple[str, int | None]]:
    """slug de quest -> (trackSlug, trackLevel) para las quests que tienen track."""
    tracks: dict[str, tuple[str, int | None]] = {}
    try:
        chunks = _split_entries(text, "QUESTS")
    except CatalogParseError:
        return tracks  # catálogo sin QUESTS: no hay tracks que heredar
    for chunk in chunks:
        slug = _field(chunk, "slug")
        track = re.search(rf"trackSlug:\s*{_STRING}", chunk)
        if not slug or not track:
            continue
        level = re.search(r"trackLevel:\s*(\d+)", chunk)
        tracks[slug] = (track.group(1), int(level.group(1)) if level else None)
    return tracks


def _badge_track(chunk: str, quest_tracks: dict) -> tuple[str | None, int | None]:
    own = re.search(rf"trackSlug:\s*{_STRING}", chunk)
    if own:  # badge de colección: su nivel es el umbral de quests del track
        threshold = re.search(r"trackCountThreshold:\s*(\d+)", chunk)
        return own.group(1), int(threshold.group(1)) if threshold else None
    track, level = None, None
    for group in re.findall(r"questSlugs:\s*\[([^\]]*)\]", chunk):
        for quest in re.findall(_STRING, group):
            qtrack, qlevel = quest_tracks.get(quest, (None, None))
            if qtrack:
                track = qtrack
                if qlevel is not None:
                    level = max(level or 0, qlevel)
    return track, level


def parse_catalog(path: Path) -> list[CatalogEntry]:
    text = path.read_text(encoding="utf-8")
    quest_tracks = _quest_tracks(text)
    entries = []
    for chunk in _split_entries(text):
        slug = _field(chunk, "slug")
        if not slug:
            continue
        image = re.search(rf"imageUrl:\s*B\({_STRING}\)", chunk)
        track, track_level = _badge_track(chunk, quest_tracks)
        entries.append(
            CatalogEntry(
                slug=slug,
                name=_field(chunk, "name") or slug,
                description=_field(chunk, "description") or "",
                criteria=_field(chunk, "criteria") or "",
                category=_field(chunk, "categorySlug") or "",
                image_file=image.group(1) if image else None,
                retired=bool(re.search(r"retire:\s*true", chunk)),
                track=track,
                track_level=track_level,
            )
        )
    if not entries:
        raise CatalogParseError("0 entradas válidas en BADGES")
    return entries


def merge_catalog(m, entries, repo_root: Path) -> list[str]:
    """Sincroniza el manifiesto con el catálogo del portal. Muta m; devuelve warnings."""
    from badgegen.manifest import Badge  # import tardío para evitar ciclo

    seen: set[str] = set()
    for entry in entries:
        if entry.retired:
            continue
        seen.add(entry.slug)
        badge = m.get(entry.slug)
        if badge is None:
            badge = Badge(slug=entry.slug, name=entry.name,
                          file=entry.image_file or default_file(entry.slug))
            m.badges.append(badge)
        badge.name = entry.name
        badge.description = entry.description
        badge.criteria = entry.criteria
        badge.category = entry.category
        badge.track = entry.track
        badge.track_level = entry.track_level
        if entry.image_file:
            badge.file = entry.image_file
        if badge.status != "regen":
            badge.status = "ok" if (repo_root / badge.file).is_file() else "missing"
    return [
        f"'{b.slug}' está en badges.yaml pero no en el catálogo activo del portal"
        for b in m.badges
        if b.slug not in seen
    ]
