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


def roundness(mask: np.ndarray) -> float:
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
