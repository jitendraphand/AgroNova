import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from render_visuals import lidar_scan, run_sim  # noqa: E402


def test_lidar_hits_circle_at_expected_range():
    ang, rng = lidar_scan((0, 0, 0), np.array([[2.0, 0.0, 0.5]]), n=360)
    assert abs(rng[np.argmin(np.abs(ang))] - 1.5) < 1e-9


def test_sim_stops_before_person_and_keeps_lane():
    field, person, frames = run_sim()
    x, y, _ = frames[-1]["pose"]
    assert frames[-1]["stop"]
    gap = math.hypot(person[0] - x, person[1] - y) - person[2] - 0.35  # robot half-length
    assert 0.0 < gap < 0.7
    ys = np.array([f["pose"][1] for f in frames[100:]])
    assert np.abs(ys).max() < 0.05
    for f in frames:  # robot body (half-width 0.31) never overlaps a plant (r 0.08) in this ideal model
        px, py, _ = f["pose"]
        near = field[np.abs(field[:, 0] - px) < 0.35]
        assert np.all(np.abs(near[:, 1] - py) > 0.31 + 0.08)
