"""Promoción de candidatos a imagen final y fix in-place de finales."""
from __future__ import annotations

import shutil
from pathlib import Path

import httpx
from PIL import Image

from badgegen import config, docs_gen, manifest as manifest_mod, postprocess
from badgegen.config import Settings
from badgegen.manifest import Manifest


def purge_cdn(file: str, client: httpx.Client | None = None) -> bool:
    client = client or httpx.Client()
    url = config.JSDELIVR_PURGE.format(file=file)
    try:
        response = client.get(url, timeout=10)
        if response.status_code < 400:
            return True
        print(f"WARNING: purge devolvió {response.status_code}; lánzalo a mano: {url}")
    except httpx.HTTPError as exc:
        print(f"WARNING: purge falló ({exc}); lánzalo a mano: {url}")
    return False


def _finish(settings: Settings, m: Manifest, badge, image: Image.Image,
            client: httpx.Client | None) -> Path:
    final = settings.repo_root / badge.file
    tmp = final.with_suffix(".tmp.png")
    image.save(tmp, format="PNG")
    tmp.replace(final)
    badge.status = "ok"
    badge.issues = []
    manifest_mod.save(m, settings.manifest_path)
    purge_cdn(badge.file, client=client)
    try:
        docs_gen.write_docs(settings, m)
    except docs_gen.MarkersMissing as exc:
        print(f"WARNING: docs no regenerados: {exc}")
    return final


def promote(settings: Settings, m: Manifest, slug: str, candidate: Path,
            keep: bool = False, client: httpx.Client | None = None) -> Path:
    badge = m.get(slug)
    if badge is None:
        raise KeyError(f"slug desconocido: {slug}")
    if not candidate.is_file():
        raise FileNotFoundError(candidate)
    processed = postprocess.process(
        Image.open(candidate), diameter=m.target_diameter
    )
    final = _finish(settings, m, badge, processed, client)
    if not keep:
        shutil.rmtree(settings.candidates_dir / slug, ignore_errors=True)
    return final


def fix(settings: Settings, m: Manifest, slug: str,
        client: httpx.Client | None = None) -> Path:
    badge = m.get(slug)
    if badge is None:
        raise KeyError(f"slug desconocido: {slug}")
    final = settings.repo_root / badge.file
    if not final.is_file():
        raise FileNotFoundError(final)
    processed = postprocess.process(Image.open(final), diameter=m.target_diameter)
    return _finish(settings, m, badge, processed, client)
