import numpy as np
from PIL import Image

from badgegen import qc


def test_perfect_circle_passes(make_badge):
    r = qc.check_image(make_badge())
    assert r.ok, r.issues
    assert r.roundness > 0.99


def test_flattened_circle_flagged(make_badge):
    r = qc.check_image(make_badge(rx=560, ry=530))
    assert "flattened-circle" in r.issues
    assert abs(r.roundness - 530 / 560) < 0.01


def test_no_transparency_flagged(make_badge):
    r = qc.check_image(make_badge(transparent_bg=False))
    assert "no-transparency" in r.issues
    # la máscara por color sigue midiendo bien la redondez
    assert r.roundness > 0.99


def test_wrong_size_flagged(make_badge):
    r = qc.check_image(make_badge(w=1024, h=1024, rx=450, ry=450))
    assert "wrong-size" in r.issues


def test_empty_image():
    r = qc.check_image(Image.new("RGBA", (1254, 1254), (0, 0, 0, 0)))
    assert "empty-image" in r.issues and not r.ok


def test_flattened_opaque_near_background_fill_flagged(make_badge):
    # interior casi negro sobre fondo negro: la máscara de color solo ve el anillo;
    # sin relleno de huecos la redondez del anillo da falso negativo (0.986 vs 0.982 real)
    r = qc.check_image(make_badge(rx=560, ry=550, transparent_bg=False))
    assert "flattened-circle" in r.issues
    assert abs(r.roundness - 550 / 560) < 0.005


def test_mask_bbox_ignores_stray_pixels(make_badge):
    im = make_badge(rx=560, ry=560)
    arr = np.asarray(im).copy()
    arr[5, 5] = [245, 196, 0, 255]  # píxel suelto en la esquina
    mask = qc.outer_mask(Image.fromarray(arr))
    x0, y0, x1, y1 = qc.mask_bbox(mask)
    assert x0 > 20 and y0 > 20  # el píxel suelto no cuenta
