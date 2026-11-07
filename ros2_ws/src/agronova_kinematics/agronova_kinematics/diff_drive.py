"""Differential-drive (skid-steer approximation) kinematics for AgroNova.

Units: SI (m, s, rad). Slip is not modelled.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# Placeholder parameters (SRS A-3, A-7) — TBD after mechanical design.
DEFAULT_WHEEL_RADIUS = 0.15
DEFAULT_TRACK_WIDTH = 0.50
MAX_LINEAR_SPEED = 1.0


@dataclass(frozen=True)
class DiffDriveParams:
    wheel_radius: float = DEFAULT_WHEEL_RADIUS
    track_width: float = DEFAULT_TRACK_WIDTH
    max_linear_speed: float = MAX_LINEAR_SPEED

    def __post_init__(self):
        if self.wheel_radius <= 0 or self.track_width <= 0:
            raise ValueError("wheel_radius and track_width must be positive")


_DEFAULT = DiffDriveParams()


def inverse(v: float, omega: float, p: DiffDriveParams = _DEFAULT):
    """Body twist (v, omega) -> wheel angular speeds (left, right) [rad/s].

    Linear speed is clamped to +/- max_linear_speed (R-008).
    """
    v = max(-p.max_linear_speed, min(p.max_linear_speed, v))
    half = p.track_width / 2.0
    return (v - omega * half) / p.wheel_radius, (v + omega * half) / p.wheel_radius


def forward(w_left: float, w_right: float, p: DiffDriveParams = _DEFAULT):
    """Wheel angular speeds -> body twist (v, omega)."""
    v = p.wheel_radius * (w_right + w_left) / 2.0
    omega = p.wheel_radius * (w_right - w_left) / p.track_width
    return v, omega


def integrate_odometry(x, y, theta, v, omega, dt, eps=1e-9):
    """Exact constant-twist pose integration over dt. Returns (x, y, theta)."""
    if abs(omega) < eps:
        x += v * dt * math.cos(theta)
        y += v * dt * math.sin(theta)
    else:
        r = v / omega
        x += r * (math.sin(theta + omega * dt) - math.sin(theta))
        y -= r * (math.cos(theta + omega * dt) - math.cos(theta))
    theta = math.atan2(math.sin(theta + omega * dt), math.cos(theta + omega * dt))
    return x, y, theta
