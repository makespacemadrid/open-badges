import numpy as np
import pytest
from PIL import Image, ImageDraw


@pytest.fixture
def make_badge():
    """Dibuja un badge sintético: anillo amarillo + disco negro, radios rx/ry."""

    def _make(w=1254, h=1254, rx=560, ry=560, cx=None, cy=None,
              transparent_bg=True, ring_width=40):
        cx = w // 2 if cx is None else cx
        cy = h // 2 if cy is None else cy
        bg = (0, 0, 0, 0) if transparent_bg else (0, 0, 0, 255)
        im = Image.new("RGBA", (w, h), bg)
        d = ImageDraw.Draw(im)
        box = (cx - rx, cy - ry, cx + rx, cy + ry)
        d.ellipse(box, fill=(10, 10, 10, 255), outline=(245, 196, 0, 255), width=ring_width)
        return im

    return _make


def png_bytes(im):
    import io

    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()
