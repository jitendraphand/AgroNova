# AgroNova System Requirements Specification (DRAFT r0.1)

## 1. Missing inputs (must be confirmed by project owner)
| ID | Missing information | Why it matters |
|---|---|---|
| MI-1 | Target crop(s) and agricultural task(s) | Drives tool interface, payload, sensors |
| MI-2 | Row spacing / field layout | Track width, ground clearance |
| MI-3 | Terrain, slope, soil, weather | Drive type, IP rating, traction |
| MI-4 | Deployment country | Applicable safety standards, radio regs |
| MI-5 | Budget per unit | Component selection |
| MI-6 | Required runtime per charge | Battery sizing |

## 2. Assumptions (explicit, unverified — revisit at Gate 1)
| ID | Assumption | Justification | Alternatives considered |
|---|---|---|---|
| A-1 | 4-wheel skid-steer, modelled as differential drive | Simple, robust, few parts; good on soil | Tracks (better traction, higher losses), Ackermann (complex) |
| A-2 | Max payload 20 kg (tool + produce) | Small-plot weeding/scouting class | 5 kg scout, 50 kg carrier |
| A-3 | Max speed 1.0 m/s | Safe walking-pace field operation | 0.5 m/s, 2 m/s |
| A-4 | Max slope 10° | Typical cultivated fields | 5°, 15° |
| A-5 | 24 V LiFePO4 battery | Safe chemistry, common motor voltage | 12 V lead-acid, 36 V Li-ion |
| A-6 | Raspberry Pi 5 + ESP32 split | Separate real-time control from ROS 2 | Jetson (if vision AI needed), STM32 |
| A-7 | Track width 0.50 m, wheel radius 0.10 m (placeholder) | Fits narrow rows | TBD with MI-2 |
| A-8 | Electronics enclosure target IP65 | Dust/rain exposure | IP54, IP67 |

## 3. Requirements
| ID | Requirement | Type |
|---|---|---|
| R-001 | Robot shall be driveable manually via teleoperation | Functional |
| R-002 | Robot shall compute wheel speeds from commanded (v, ω) | Functional |
| R-003 | Robot shall estimate pose from wheel odometry | Functional |
| R-004 | Hardware E-stop shall remove motor power independent of software | Safety |
| R-005 | Motors shall stop within 500 ms (TBD) of communication loss | Safety |
| R-006 | Every printed part shall fit Neptune 4 Max usable envelope (400×400×460 mm, 10 mm margin assumption) | Manufacturing |
| R-007 | Robot shall provide a standard tool mounting interface | Functional |
| R-008 | Max speed ≤ 1.0 m/s (A-3) | Performance |
| R-009 | Robot shall be described in URDF for simulation/visualization | Software |
| R-010 | Electronics enclosure IP65 (A-8) | Environmental |

## 4. Traceability matrix
| Req | Design implementation | Verification | Status |
|---|---|---|---|
| R-001 | ROS 2 /cmd_vel → firmware (planned) | TC-SW-010 teleop test | NOT STARTED |
| R-002 | `agronova_kinematics.diff_drive.inverse` | `test_diff_drive.py` (unit, simulated) | TESTED (unit only) |
| R-003 | `agronova_kinematics.diff_drive.integrate_odometry` | `test_diff_drive.py` | TESTED (unit only) |
| R-004 | docs/safety/SAFETY.md E-stop chain (design TBD) | TC-SAF-001 physical test | NOT STARTED |
| R-005 | firmware watchdog `CMD_TIMEOUT_MS` | TC-FW-002 bench test | NOT STARTED |
| R-006 | `tools/check_printability.py` | CI + `tests/test_printability.py` | TESTED (tool only; no parts yet) |
| R-007 | Mechanical tool interface (TBD) | TC-MECH-005 | NOT STARTED |
| R-008 | `MAX_LINEAR_SPEED` clamp in kinematics | `test_diff_drive.py` | TESTED (unit only) |
| R-009 | `agronova_description/urdf/agronova.urdf.xacro` | xacro/check_urdf in CI (planned) | IN PROGRESS |
| R-010 | Enclosure design TBD | TC-ENV-001 spray test | NOT STARTED |
