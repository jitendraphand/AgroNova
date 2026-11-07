import math

import pytest

from agronova_kinematics.diff_drive import DiffDriveParams, forward, integrate_odometry, inverse

P = DiffDriveParams(0.1, 0.5, 1.0)


@pytest.mark.parametrize("v,w", [(0.5, 0.0), (0.0, 1.0), (0.3, -0.7), (-0.8, 0.2)])
def test_roundtrip(v, w):
    assert forward(*inverse(v, w, P), P) == pytest.approx((v, w))


def test_straight():
    assert inverse(0.5, 0.0, P) == pytest.approx((5.0, 5.0))


def test_spin_in_place():
    wl, wr = inverse(0.0, 1.0, P)
    assert wl == pytest.approx(-2.5) and wr == pytest.approx(2.5)


def test_speed_clamp():
    v, _ = forward(*inverse(5.0, 0.0, P), P)
    assert v == pytest.approx(1.0)


def test_odometry_full_circle_returns_home():
    x = y = th = 0.0
    for _ in range(1000):
        x, y, th = integrate_odometry(x, y, th, 0.5, 2 * math.pi / 10, 0.01)
    assert (x, y) == pytest.approx((0.0, 0.0), abs=1e-9)


def test_odometry_quarter_circle():
    x, y, th = integrate_odometry(0, 0, 0, 1.0, math.pi / 2, 1.0)
    r = 1.0 / (math.pi / 2)
    assert (x, y, th) == pytest.approx((r, r, math.pi / 2))


def test_invalid_params():
    with pytest.raises(ValueError):
        DiffDriveParams(0, 0.5)
