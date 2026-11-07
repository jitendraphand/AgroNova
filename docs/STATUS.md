# Project status
Status vocabulary: NOT STARTED · IN PROGRESS · BLOCKED · TESTED · PASSED · FAILED · NOT APPLICABLE

| Phase | Status | Gate | Evidence |
|---|---|---|---|
| 1 Requirements & feasibility | IN PROGRESS | Gate 1 — NOT STARTED | docs/requirements/SRS.md (draft) |
| 2 System architecture | IN PROGRESS (baseline proposed) | Gate 2 — NOT STARTED | README, docs/* |
| 3 Detailed design | NOT STARTED (software skeletons only) | Gate 3 — NOT STARTED | — |
| 4 Simulation | NOT STARTED | Gate 4 — NOT STARTED | — |
| 5 Manufacturing prep | NOT STARTED | Gate 5 — NOT STARTED | — |
| 6 Physical prototype | NOT STARTED | Gate 6 — NOT STARTED | — |
| 7 QA/QC & validation | NOT STARTED | Gate 7 — NOT STARTED | — |
| 8 Release | NOT STARTED | Gate 8 — NOT STARTED | — |

Functionality maturity: **planned** (most), **implemented** (diff-drive kinematics, printability checker, URDF skeleton, firmware skeleton), **simulated** (none), **manufactured** (none), **physically validated** (none).

## Automated verification log (2026-11-07, local box)
| Check | Result |
|---|---|
| `ruff check .` | All checks passed |
| `pytest -q` (kinematics + printability tool) | 15 passed (unit/numerical only — not hardware) |
| `xacro agronova.urdf.xacro` | Expands without error |
| `pio run` (esp32dev, espressif32 8.0.0) | Build SUCCESS — not flashed/tested on hardware |
| `colcon build` (ROS 2 Jazzy) | Not run locally (no ROS install on box); runs in CI |
