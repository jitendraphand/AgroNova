import math
import sys
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from sizing import (  # noqa: E402
    Inputs,
    battery,
    frame_beam,
    tipping,
    traction_force_n,
    tube_section,
    wheel_rpm,
    wire,
)

I0 = Inputs()


def test_flat_no_accel_is_rolling_only():
    i = replace(I0, slope_deg=0, accel_mps2=0)
    assert traction_force_n(i) == pytest.approx(65 * 9.81 * 0.10)


def test_rpm():
    assert wheel_rpm(replace(I0, v_max_mps=math.pi * 0.3, wheel_radius_m=0.15)) == pytest.approx(60)


def test_tube_section_matches_hand_calc():
    second_moment, _ = tube_section(I0)
    assert second_moment == pytest.approx((0.025**4 - 0.022**4) / 12)


def test_frame_fos_above_2():
    assert frame_beam(I0)["fos"] > 2.0


def test_tipping_exceeds_slope():
    assert tipping(I0)["lateral_tip_deg"] > I0.slope_deg


def test_battery_monotonic_in_runtime():
    assert battery(replace(I0, runtime_h=8))["capacity_ah"] > battery(I0)["capacity_ah"]


def test_wire_drop_decreases_with_area():
    assert wire(I0, 10, 20)["drop_v"] < wire(I0, 4, 20)["drop_v"]
