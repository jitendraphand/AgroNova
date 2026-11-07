# Inspection & Test Plans (ITP), FAT, SAT (r0.2)
Every result field below is empty: **no test has been executed.** Status = NOT STARTED unless noted.

## Inspection (incoming / in-process)
| ID | Item | Method | Acceptance | Status |
|---|---|---|---|---|
| INS-001 | Frame welds | Visual + 1 m straightedge | No cracks/porosity; flatness ≤ 2 mm over 700 mm | NOT STARTED |
| INS-002 | Frame dimensions | Tape/caliper vs CAD | ±1 mm overall | NOT STARTED |
| INS-010 | Guards fitted | Visual | All rotating parts guarded | NOT STARTED |
| INS-020 | Printed parts | Caliper vs STEP, visual | ±0.3 mm (small), ±0.5 mm (covers); no delamination | NOT STARTED |
| INS-030 | Wiring | Continuity, labels vs WIRING.md | 100 % match; insulation ≥ 1 MΩ at 100 V (A-28) | NOT STARTED |

## Factory Acceptance Tests (bench / workshop)
| ID | Objective | Preconditions | Equipment | Procedure | Expected / acceptance |
|---|---|---|---|---|---|
| TC-ELEC-001 | Power-up sequence | Wired, fuses fitted, wheels off ground | DMM | SW1 on; measure 24 V, 5 V, 3.3 V rails | Within ±5 %; K1 open until RESET |
| TC-ELEC-003 | Fuse coordination | — | Bench supply with limit | Short-circuit test on dummy load per procedure (TBD) | Only branch fuse opens |
| TC-ELEC-005 | Motor thermal | Robot loaded to 65 kg on 10° ramp | IR thermometer | Drive 30 min | Motor case < manufacturer limit (TBD) |
| TC-SAF-001 | E-stop | Wheels off ground, running 0.5 m/s | Stopwatch/scope | Press ES1, ES2 each 10× | Motor power removed every time; < 0.5 s to stop wheels (target) |
| TC-SAF-002 | Remote E-stop & range | Open field | — | Trigger at 10/30/50 m; switch off transmitter | Stop every time |
| TC-SAF-005 | Speed limit | Ground run | GNSS/odometry log | Command 2 m/s | Measured ≤ 1.0 m/s |
| TC-FW-002 | Comms-loss stop | Driving 0.5 m/s | Scope on PWM | Unplug USB | PWM = 0 within 0.5 s + one 10 ms loop |
| TC-FW-003 | Speed PID | Wheels off ground then on soil | Log `S` messages | Step 0→3 rad/s | Steady error < 2 %, overshoot < 15 % |
| TC-MECH-004 | CoG measurement | Assembled, loaded | 4 scales, lift | Weigh at each wheel level and tilted | Record CoG; update A-10 |
| TC-MECH-006 | Rolling resistance | Field soil | Spring scale/load cell | Tow at constant speed | Record Crr; update A-12 |
| TC-ENV-001 | Water spray | Enclosure closed | Hose per IP65-like method (TBD) | 3 min all directions | No water inside |

## Site Acceptance Tests (Maharashtra field, supervised)
| ID | Objective | Acceptance |
|---|---|---|
| SAT-001 | Teleop traverse 50 m inter-row, cotton 90 cm | No plant contact, no stall |
| SAT-002 | Headland turn | Completes within 2 m headland |
| SAT-003 | Runtime | ≥ 4 h mixed duty on one charge (R-?, A-16) |
| SAT-004 | Autonomous row (supervised) | 10 rows, cross-track error ≤ 0.10 m |
| SAT-005 | Person-in-path stop | Stops before 0.6 m, 10/10 |

Result record template: `docs/testing/README.md`. Store evidence (logs, photos, video) under `test_reports/<TestID>/<date>/`.

## NCR / CAPA templates
NCR: ID · date · item/part no. · requirement violated · description · evidence · disposition (use-as-is/rework/scrap) · approver.
CAPA: ID · linked NCR · root cause (5-why) · corrective action · preventive action · due date · verification of effectiveness · closed by.
