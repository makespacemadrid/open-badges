"""QC geométrico de imágenes de badge: tamaño, transparencia, redondez."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from PIL import Image

from badgegen import config


def outer_mask(im: Image.Image) -> np.ndarray:
    arr = np.asarray(im.convert("RGBA"))
    alpha = arr[:, :, 3]
    if alpha.min() < 128:  # hay transparencia real
        return alpha > 128
    rgb = arr[:, :, :3].astype(int)
    corners = np.array([rgb[0, 0], rgb[0, -1], rgb[-1, 0], rgb[-1, -1]])
    bg = np.median(corners, axis=0)
    return np.abs(rgb - bg).sum(axis=2) > 60


def mask_bbox(mask: np.ndarray, min_count: int = 3) -> tuple[int, int, int, int]:
    cols = np.nonzero(mask.sum(axis=0) >= min_count)[0]
    rows = np.nonzero(mask.sum(axis=1) >= min_count)[0]
    if len(cols) == 0 or len(rows) == 0:
        raise ValueError("máscara vacía")
    return int(cols[0]), int(rows[0]), int(cols[-1]), int(rows[-1])


def _fill_spans(mask: np.ndarray) -> np.ndarray:
    """Rellena huecos interiores: span por filas AND span por columnas."""

    def _span(m: np.ndarray, axis: int) -> np.ndarray:
        fwd = np.maximum.accumulate(m, axis=axis)
        bwd = np.flip(np.maximum.accumulate(np.flip(m, axis=axis), axis=axis), axis=axis)
        return fwd & bwd

    return _span(mask, 0) & _span(mask, 1)


def roundness(mask: np.ndarray) -> float:
    mask = _fill_spans(mask)
    ys, xs = np.nonzero(mask)
    if len(xs) < 10:
        return 0.0
    cov = np.cov(np.stack([xs - xs.mean(), ys - ys.mean()]))
    ev = np.linalg.eigvalsh(cov)
    if ev[1] <= 0:
        return 0.0
    return float((max(ev[0], 0.0) / ev[1]) ** 0.5)


@dataclass
class QCResult:
    roundness: float = 0.0
    issues: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues


def check_image(im: Image.Image, *, canvas: int = config.CANVAS_SIZE,
                threshold: float = config.ROUNDNESS_THRESHOLD) -> QCResult:
    result = QCResult()
    if im.size != (canvas, canvas):
        result.issues.append("wrong-size")
    rgba = im.convert("RGBA")
    if np.asarray(rgba)[:, :, 3].min() >= 128:
        result.issues.append("no-transparency")
    mask = outer_mask(rgba)
    if mask.sum() < 100:
        result.issues.append("empty-image")
        return result
    result.roundness = roundness(mask)
    if result.roundness < threshold:
        result.issues.append("flattened-circle")
    return result


import base64 as _base64
import json as _json

import httpx as _httpx

JUDGE_PROMPT = """Eres un revisor de calidad de insignias (badges) circulares.
Evalúa SOLO la legibilidad y limpieza de esta imagen de badge:
- ¿El texto se lee sin esfuerzo? ¿Está bien escrito (sin letras deformadas o inventadas)?
- ¿La tipografía está entera (sin trazos rotos ni glifos corruptos)?
- ¿Hay ruido, artefactos o texturas sucias?
- ¿El contraste figura/fondo es alto?
Responde en JSON: {"score": <entero 1-5, 5 = perfecto>, "issues": ["problema en español", ...]}.
Si score >= 4, issues debe ser [] o muy corto."""


@dataclass
class JudgeResult:
    score: int
    issues: list[str] = field(default_factory=list)


def judge_legibility(png: bytes, api_key: str, model: str = "gemini-2.5-flash",
                     client: _httpx.Client | None = None) -> JudgeResult:
    from badgegen.providers.base import ProviderError, post_with_retry

    client = client or _httpx.Client()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {
        "contents": [{"parts": [
            {"text": JUDGE_PROMPT},
            {"inline_data": {"mime_type": "image/png",
                             "data": _base64.b64encode(png).decode()}},
        ]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    response = post_with_retry(client, url, json=body,
                               headers={"x-goog-api-key": api_key})
    try:
        text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        verdict = _json.loads(text)
        return JudgeResult(score=int(verdict["score"]),
                           issues=[str(i) for i in verdict.get("issues", [])])
    except (KeyError, IndexError, ValueError, TypeError) as exc:
        raise ProviderError(f"veredicto ilegible del juez: {exc}") from exc
