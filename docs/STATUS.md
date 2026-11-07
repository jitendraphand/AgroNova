# Project status
Status vocabulary: NOT STARTED · IN PROGRESS · BLOCKED · TESTED · PASSED · FAILED · NOT APPLICABLE

| Phase | Status | Gate | Evidence |
|---|---|---|---|
| 1 Requirements & feasibility | IN PROGRESS | Gate 1 — NOT STARTED | docs/requirements/SRS.md (draft) |
| 2 System architecture | IN PROGRESS (baseline proposed) | Gate 2 — NOT STARTED | README, docs/* |
| 3 Detailed design | IN PROGRESS (draft CAD, calcs, firmware PID, wiring) | Gate 3 — NOT STARTED | — |
| 4 Simulation | IN PROGRESS (Gazebo sim runs headless; open-loop drive captured; Gate 4 tests not executed) | Gate 4 — NOT STARTED | — |
| 5 Manufacturing prep | NOT STARTED | Gate 5 — NOT STARTED | — |
| 6 Physical prototype | NOT STARTED | Gate 6 — NOT STARTED | — |
| 7 QA/QC & validation | NOT STARTED | Gate 7 — NOT STARTED | — |
| 8 Release | NOT STARTED | Gate 8 — NOT STARTED | — |

Functionality maturity: **planned** (most), **implemented** (diff-drive kinematics, printability checker, sizing calcs, draft CAD for frame + 5 printed parts, URDF + Gazebo plugins, firmware PID/encoders/watchdog, Nav2/EKF configs), **simulated** (open-loop straight drive in Gazebo with EKF running; Python kinematic stop-zone demo), **manufactured** (none), **physically validated** (none).

## Automated verification log (2026-11-07, local box, Asia/Calcutta)
| Check | Result |
|---|---|
| `ruff check .` | All checks passed |
| `pytest -q` | 52 passed (unit / static / model-only — not hardware) |
| CadQuery build | 7 STEP + 5 STL generated, all solids valid; all STL FIT 400×400×460 envelope |
| `pio run` (esp32dev, espressif32 8.0.0) | Build SUCCESS — not flashed |
| PID host test (zig c++) | Passed on assumed first-order motor model |
| `colcon build` (RoboStack Jazzy via pixi) | 5 packages built |
| `colcon test` agronova_kinematics | 10 passed |
| Gazebo Harmonic headless run + RViz2 | Ran; visuals in docs/media (open-loop drive only) |
| Nav2 | NOT RUN |
