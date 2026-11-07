# Calibration procedures (r0.2 — not yet performed)
| ID | What | Procedure | Output |
|---|---|---|---|
| CAL-001 | Wheel radius | Mark tyre, drive straight 10 m on site soil under load, count revs (or encoder counts); r = d / (2π·revs) | `wheel_radius` param (launch + firmware) |
| CAL-002 | Encoder counts/rev | Wheels off ground, rotate wheel exactly 10 turns by hand, read count | `COUNTS_PER_WHEEL_REV` in firmware |
| CAL-003 | Effective track width (skid-steer) | Command spin in place 10 full turns (count with marker), compute b_eff = r·Δθ_wheels / Δθ_body | `track_width` param — expect > geometric 0.50 m due to slip |
| CAL-004 | Motor direction | Command +1 rad/s each side | Both wheels forward; else swap DIR logic/motor leads |
| CAL-005 | IMU | Static 60 s level; record bias; set mounting orientation | ekf.yaml / driver params |
| CAL-006 | Lidar extrinsic | Measure lidar_joint offset with tape vs base_link; verify with wall at known distance | URDF `lidar_joint` origin |
| CAL-007 | GNSS antenna offset & datum | Measure offset; set magnetic_declination for site | URDF `gps_joint`, ekf.yaml |
| CAL-008 | PID | See docs/firmware/README.md | Gains in main.cpp |
Record each calibration with date, operator, values before/after.
