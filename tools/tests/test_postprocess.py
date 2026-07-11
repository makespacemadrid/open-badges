import numpy as np
import pytest
from PIL import Image

from badgegen import postprocess, qc


def _disk_info(im):
    return postprocess.analyze(im)


def test_analyze_reports_ellipse(make_badge):
    info = _disk_info(make_badge(rx=560, ry=530))
    assert abs(info.ratio - 530 / 560) < 0.01
    assert abs(info.cx - 627) < 3 and abs(info.cy - 627) < 3


def test_process_circularizes_and_centers(make_badge):
    # descentrado pero sin recortar: x 600±560 = 40..1160, y 650±535 = 115..1185
    out = postprocess.process(make_badge(rx=560, ry=535, cx=600, cy=650))
    assert out.size == (1254, 1254)
    info = _disk_info(out)
    assert info.ratio > 0.99
    assert abs(info.w - 1180) <= 4
    assert abs(info.cx - 626.5) < 3 and abs(info.cy - 626.5) < 3
    corners = np.asarray(out)[:, :, 3]
    assert corners[0, 0] == 0 and corners[-1, -1] == 0


def test_process_opaque_background_gets_transparency(make_badge):
    out = postprocess.process(make_badge(transparent_bg=False))
    alpha = np.asarray(out)[:, :, 3]
    assert alpha[0, 0] == 0  # esquinas transparentes
    assert alpha[627, 627] == 255  # centro opaco
    assert qc.check_image(out).ok


def test_process_idempotent(make_badge):
    once = postprocess.process(make_badge(rx=560, ry=540))
    twice = postprocess.process(once)
    i1, i2 = _disk_info(once), _disk_info(twice)
    assert abs(i1.w - i2.w) <= 2 and abs(i1.h - i2.h) <= 2
    assert i2.ratio > 0.99


def test_process_rejects_irrecoverable(make_badge):
    with pytest.raises(postprocess.ShapeError):
        postprocess.process(make_badge(rx=560, ry=500))  # ratio 0.892 < 0.95
