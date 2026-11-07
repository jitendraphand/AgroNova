# AgroNova — Open-Source Agricultural Robot

AgroNova is a modular, open-source agricultural robotics platform: field mobility, interchangeable tools, sensors, manual + autonomous operation, and remote diagnostics.

> **Project status: Phase 1 (Requirements & feasibility).** Nothing here has been manufactured or physically validated. See [docs/STATUS.md](docs/STATUS.md).

## Baseline architecture (proposed, pending Gate 1 review)
```
 Operator / Ground station ──(Wi‑Fi/LTE, ROS 2 DDS)──┐
                                                     ▼
  High-level computer (Raspberry Pi 5 baseline, TBD) — ROS 2 Jazzy
   ├─ agronova_kinematics (diff-drive FK/IK, odometry)
   ├─ Nav2 / robot_localization (planned)
   └─ agronova_bringup, agronova_description (URDF)
                     │ UART / micro-ROS (TBD)
                     ▼
  Real-time controller (ESP32 baseline, TBD) — firmware/motor_controller
   ├─ motor drivers → 4× DC gearmotors (skid-steer)  [models TBD]
   ├─ encoders, watchdog, comms-loss stop
   └─ HARDWARE E-stop chain cuts motor power independently of software
```

## Repository layout
| Path | Contents |
|---|---|
| `docs/requirements/` | SRS, assumptions, traceability matrix |
| `docs/{mechanical,electronics,firmware,ros2,simulation,kinematics,testing,manufacturing,deployment,safety}` | Discipline docs |
| `ros2_ws/src/` | ROS 2 packages (description, bringup, kinematics) |
| `firmware/motor_controller/` | PlatformIO ESP32 motor-controller skeleton |
| `hardware/` | CAD / STL / PCB (empty until real artifacts exist) |
| `bom/` | BOM templates (all parts TBD) |
| `tools/` | `check_printability.py` — STL vs Neptune 4 Max envelope |
| `tests/` | Repo-level Python tests |

## Quick start
```bash
pip install numpy pytest numpy-stl ruff
pytest -q                               # kinematics + tool tests
# ROS 2 (Jazzy): cd ros2_ws && colcon build && colcon test
# Firmware: cd firmware/motor_controller && pio run
```

## Development phases
Phases 1–8 and Gates 1–8 are tracked in [docs/STATUS.md](docs/STATUS.md). No gate is marked complete without evidence.

License: MIT. Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
