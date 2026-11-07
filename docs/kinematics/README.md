# Kinematics
No manipulator arm (not required by baseline; SRS A-1). Mobile base modelled as differential drive (skid-steer approximation; slip ignored — known limitation).

Parameters: wheel radius r, track width b.
- Inverse: ω_L = (v − ω·b/2)/r, ω_R = (v + ω·b/2)/r
- Forward: v = r(ω_R+ω_L)/2, ω = r(ω_R−ω_L)/b
- Odometry (exact arc integration): if |ω|>ε: x += v/ω·(sin(θ+ωΔt) − sin θ), y −= v/ω·(cos(θ+ωΔt) − cos θ); else straight line.
Implementation: `ros2_ws/src/agronova_kinematics/agronova_kinematics/diff_drive.py`; tests in `.../test/`. Skid-steer slip coefficient calibration: TBD (field data needed).
