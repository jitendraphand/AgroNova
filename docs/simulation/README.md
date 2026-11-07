# Simulation (r0.2) — files created, NOT yet run
| Item | File |
|---|---|
| Field world (4 cotton rows, 0.90 m spacing, Vidarbha lat/long for NavSat) | `ros2_ws/src/agronova_gazebo/worlds/cotton_field.sdf` (regenerate: `scripts/make_field_world.py --rows N`) |
| Sim sensors/plugins (diff-drive, IMU, 2D lidar, NavSat) | `agronova_description/urdf/agronova_gazebo.xacro` (included when `sim:=true`) |
| ROS↔gz bridge | `agronova_gazebo/config/bridge.yaml` |
| Launch | `ros2 launch agronova_gazebo sim.launch.py` then `ros2 launch agronova_navigation navigation.launch.py` |

Target: ROS 2 Jazzy + Gazebo Harmonic. **Status: NOT STARTED (never executed)** — the box used to author this has no ROS/Gazebo. Static checks (YAML/SDF/URDF parse, xacro expansion) run in `tests/test_ros_configs.py`.

## Gate 4 acceptance tests (planned)
| ID | Test | Acceptance |
|---|---|---|
| TC-SIM-001 | Robot spawns, `/scan`, `/imu`, `/gps/fix`, `/wheel/odom` publish | All topics at ≥ 80 % nominal rate |
| TC-SIM-002 | Odometry vs `agronova_kinematics` on 1 m straight / 90° turn | Error < 2 % / < 3° |
| TC-SIM-003 | Nav2 goal 10 m down inter-row | Reaches within 0.15 m, no plant collision, 10/10 runs |
| TC-SIM-004 | Obstacle (person model) placed in row | collision_monitor stops robot before 0.6 m |
| TC-SIM-005 | Kill cmd_vel publisher | Robot stops (sim watchdog) |
