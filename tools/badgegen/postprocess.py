"""Normalización de badges: circularizar el disco, centrar y enmascara alpha."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw

from badgegen import config, qc


class ShapeError(Exception):
    pass


@dataclass
class DiskInfo:
    x0: int
    y0: int
    x1: int
    y1: int

    @property
    def w(self) -> int:
        return self.x1 - self.x0 + 1

    @property
    def h(self) -> int:
        return self.y1 - self.y0 + 1

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2

    @property
    def ratio(self) -> float:
        return min(self.w, self.h) / max(self.w, self.h)


def analyze(im: Image.Image) -> DiskInfo:
    mask = qc.outer_mask(im)
    try:
        x0, y0, x1, y1 = qc.mask_bbox(mask)
    except ValueError as exc:
        raise ShapeError("no se detecta ningún disco en la imagen") from exc
    return DiskInfo(x0, y0, x1, y1)


def _circle_alpha(canvas: int, diameter: int) -> np.ndarray:
    """Máscara circular antialiased (supersampling 4x)."""
    scale = 4
    big = Image.new("L", (canvas * scale, canvas * scale), 0)
    d = ImageDraw.Draw(big)
    c = canvas * scale / 2
    r = (diameter / 2 + 1) * scale
    d.ellipse((c - r, c - r, c + r, c + r), fill=255)
    return np.asarray(big.resize((canvas, canvas), Image.LANCZOS))


def process(im: Image.Image, *, canvas: int = config.CANVAS_SIZE,
            diameter: int = config.TARGET_DIAMETER,
            min_ratio: float = config.MIN_FIXABLE_RATIO) -> Image.Image:
    im = im.convert("RGBA")
    info = analyze(im)
    if info.ratio < min_ratio:
        raise ShapeError(
            f"disco demasiado deformado (ratio {info.ratio:.3f} < {min_ratio}); regenerar"
        )
    # 1. Escala anisotrópica: el disco pasa a medir `diameter` en ambos ejes.
    sx, sy = diameter / info.w, diameter / info.h
    resized = im.resize(
        (max(1, round(im.width * sx)), max(1, round(im.height * sy))), Image.LANCZOS
    )
    info2 = analyze(resized)
    # 2. Centrar el disco en el lienzo.
    out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    ox = round(canvas / 2 - info2.cx)
    oy = round(canvas / 2 - info2.cy)
    out.paste(resized, (ox, oy), resized)
    # 3. Máscara circular: fuera del disco todo transparente.
    arr = np.asarray(out).copy()
    arr[:, :, 3] = np.minimum(arr[:, :, 3], _circle_alpha(canvas, diameter))
    return Image.fromarray(arr)
