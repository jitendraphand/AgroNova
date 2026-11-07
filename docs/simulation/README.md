# Simulation (r0.3)
| Item | File |
|---|---|
| Field world (4 cotton rows, 0.90 m spacing, Vidarbha lat/long for NavSat) | `ros2_ws/src/agronova_gazebo/worlds/cotton_field.sdf`; `cotton_field_capture.sdf` adds 2 static documentation cameras (regenerate: `scripts/make_field_world.py [--cameras] -o ...`) |
| Sim sensors/plugins (diff-drive, IMU, 2D lidar, NavSat) | `agronova_description/urdf/agronova_gazebo.xacro` (included when `sim:=true`) |
| ROS↔gz bridge | `agronova_gazebo/config/bridge.yaml` |
| Launch | `ros2 launch agronova_gazebo sim.launch.py [world:=cotton_field_capture.sdf] [headless:=true]` then `ros2 launch agronova_navigation navigation.launch.py` |

Target: ROS 2 Jazzy + Gazebo Harmonic (gz-sim 8.10.0), installed via RoboStack/pixi (`tools/ros_env/pixi.toml`).

**Status (2026-11-07):** workspace builds with `colcon build` (5 packages); `colcon test` for agronova_kinematics: 10 passed. The sim was launched headless and the robot was driven straight down the inter-row lane with a constant `cmd_vel` (0.5 m/s) — **open-loop, Nav2 was NOT run**. The local EKF (robot_localization) ran during the capture. The Gate 4 acceptance tests below have NOT been executed as formal tests.

Observations from the capture run (informal, not acceptance evidence): Gazebo `/wheel/odom` reported 6.46 m travelled in a ~16 s wall-clock command window (sim ran slower than real time under software rendering), lateral drift 0.000 m (ideal straight-line drive on a flat plane with no slip model). In RViz the EKF position covariance (magenta) grows along the run because the local EKF fuses only velocities — expected; absolute correction comes from GNSS in the global EKF.

## Visuals
| File | Produced by | Real sim? |
|---|---|---|
| `docs/media/gazebo_overview.gif`, `gazebo_top.gif`, `gazebo/*.png` | Gazebo Harmonic camera sensors (ogre2, `--headless-rendering`) in `worlds/cotton_field_capture.sdf`, saved by `tools/gazebo_capture.py` | Yes — Gazebo |
| `docs/media/rviz.gif`, `rviz/rviz_6.png` | RViz2 (`rviz/agronova_sim.rviz`) under Xvfb, screen-grabbed with ffmpeg x11grab during the same run | Yes — RViz2 on live sim topics |
| `docs/media/gazebo_odom_scan.png` | matplotlib plot of `/wheel/odom` and `/scan` recorded from the run (`gazebo/run_log.npz`) | Data from Gazebo |
| `docs/media/kinematic_sim.gif`, `kinematic_sim_final.png` | `tools/render_visuals.py`: 2D kinematic sim using `agronova_kinematics` + ideal ray-cast lidar + stop zone, simple lane-keeping law | No — Python kinematic model |
| `docs/media/urdf_in_field.png` | `tools/render_visuals.py`: xacro-expanded URDF primitives drawn with matplotlib | No — static render |
| `docs/media/cad_assembly.png` | `tools/render_visuals.py`: CadQuery geometry tessellated, drawn with matplotlib | No — static render |

Regenerate: `tools/capture_gazebo.sh` (Gazebo/RViz; needs pixi, Xvfb, ffmpeg) and `python tools/render_visuals.py` (CadQuery + matplotlib).

## Gate 4 acceptance tests (planned)
| ID | Test | Acceptance |
|---|---|---|
| TC-SIM-001 | Robot spawns, `/scan`, `/imu`, `/gps/fix`, `/wheel/odom` publish | All topics at ≥ 80 % nominal rate |
| TC-SIM-002 | Odometry vs `agronova_kinematics` on 1 m straight / 90° turn | Error < 2 % / < 3° |
| TC-SIM-003 | Nav2 goal 10 m down inter-row | Reaches within 0.15 m, no plant collision, 10/10 runs |
| TC-SIM-004 | Obstacle (person model) placed in row | collision_monitor stops robot before 0.6 m |
| TC-SIM-005 | Kill cmd_vel publisher | Robot stops (sim watchdog) |
