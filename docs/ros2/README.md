# ROS 2
Target distro: Jazzy (Ubuntu 24.04). Packages:
- `agronova_description` — URDF/xacro, RViz display launch.
- `agronova_bringup` — top-level launch.
- `agronova_kinematics` — ament_python; diff-drive FK/IK library + `diff_drive_node` (/cmd_vel → wheel speeds, odometry).
Planned: Nav2, robot_localization (EKF + GNSS), ros2_control hardware interface.

## r0.2 additions
- `agronova_gazebo` — world, bridge, `sim.launch.py`.
- `agronova_navigation` — `ekf.yaml` (local EKF: wheel odom + IMU; global EKF + navsat_transform: GNSS), `nav2_params.yaml` (Regulated Pure Pursuit, Smac 2D, collision monitor stop zone), `localization.launch.py`, `navigation.launch.py`.
All parameters untuned; not executed yet (see docs/simulation).
