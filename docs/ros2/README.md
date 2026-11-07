# ROS 2
Target distro: Jazzy (Ubuntu 24.04). Packages:
- `agronova_description` — URDF/xacro, RViz display launch.
- `agronova_bringup` — top-level launch.
- `agronova_kinematics` — ament_python; diff-drive FK/IK library + `diff_drive_node` (/cmd_vel → wheel speeds, odometry).
Planned: Nav2, robot_localization (EKF + GNSS), ros2_control hardware interface.
