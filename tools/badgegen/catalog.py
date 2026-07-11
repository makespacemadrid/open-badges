"""Parser del catálogo TypeScript del portal (const BADGES: BadgeSpec[])."""
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
    track: str
    image_file: str | None
    retired: bool


def default_file(slug: str) -> str:
    return f"{slug}.png" if slug.startswith("badge-") else f"badge-{slug}.png"


def _split_entries(text: str) -> list[str]:
    """Devuelve los literales {...} de primer nivel del array BADGES.

    Scanner de caracteres consciente de strings ('", `) con escapes y de
    anidamiento de llaves/corchetes: los regex no valen porque las entradas
    contienen questGroups: [{...}] anidados.
    """
    marker = re.search(r"const\s+BADGES\s*:[^=]*=\s*\[", text)
    if not marker:
        raise CatalogParseError("no se encontró 'const BADGES' en el catálogo")
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
        raise CatalogParseError("0 entradas en BADGES: ¿cambió el formato del catálogo?")
    return entries


_STRING = r"'((?:[^'\\]|\\.)*)'"


def _field(chunk: str, key: str) -> str | None:
    m = re.search(rf"(?<![A-Za-z]){key}:\s*{_STRING}", chunk, re.DOTALL)
    if not m:
        return None
    return m.group(1).replace("\\'", "'").replace("\\\\", "\\")


def parse_catalog(path: Path) -> list[CatalogEntry]:
    text = path.read_text(encoding="utf-8")
    entries = []
    for chunk in _split_entries(text):
        slug = _field(chunk, "slug")
        if not slug:
            continue
        image = re.search(rf"imageUrl:\s*B\({_STRING}\)", chunk)
        entries.append(
            CatalogEntry(
                slug=slug,
                name=_field(chunk, "name") or slug,
                description=_field(chunk, "description") or "",
                criteria=_field(chunk, "criteria") or "",
                track=_field(chunk, "categorySlug") or "",
                image_file=image.group(1) if image else None,
                retired=bool(re.search(r"retire:\s*true", chunk)),
            )
        )
    if not entries:
        raise CatalogParseError("0 entradas válidas en BADGES")
    return entries
