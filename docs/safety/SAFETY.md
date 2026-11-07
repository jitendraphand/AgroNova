# Safety engineering (r0.2 — design, NOT validated)

## Principles
1. Hardware E-stop chain de-energises motor contactor K1 independently of all software (docs/electronics/WIRING.md).
2. Software watchdog (firmware, 500 ms) is an additional layer, never a substitute.
3. Safe startup: K1 open at power-up until manual RESET; firmware outputs zero until a valid command arrives.
4. No unsupervised autonomous operation before Gate 7 safety tests pass with recorded evidence.

## Safety functions
| ID | Function | Implementation | Verification | Status |
|---|---|---|---|---|
| SF-1 | Emergency stop (2 physical buttons) | ES1, ES2 NC in series → K2 → K1 | TC-SAF-001 | NOT STARTED |
| SF-2 | Remote E-stop | Wireless E-stop receiver NC contact RX1 in chain (fail-safe on signal loss — must be a property of the chosen product, verify) | TC-SAF-002 | NOT STARTED |
| SF-3 | Comms-loss stop | Firmware CMD_TIMEOUT_MS | TC-FW-002 | NOT STARTED |
| SF-4 | Obstacle/person stop | Nav2 collision_monitor stop zone 0.6 m | TC-SIM-004, TC-SAF-004 | NOT STARTED |
| SF-5 | Overcurrent | F1–F5 fuses + BMS | TC-ELEC-003 | NOT STARTED |
| SF-6 | Moving-part guards | Wheel guards/tool guard (CAD TBD) | Inspection INS-010 | NOT STARTED |
| SF-7 | Speed limit 1.0 m/s | Kinematics clamp + firmware clamp | unit tests (TESTED) + TC-SAF-005 (physical) | IN PROGRESS |

## Standards to assess (applicability TBD — deployment India)
ISO 12100 (risk assessment), ISO 13849-1 (safety-related control PL), IEC 60204-1 (electrical equipment of machines), ISO 18497 (autonomous agricultural machinery safety), ISO 4254-1 (agricultural machinery safety), IS/IEC 62133 / UN 38.3 for battery transport, WPC rules for radio equipment in India. Not yet reviewed in detail.

## Safe maintenance
Turn SW1 off and remove the battery connector (lock-out) before touching drivers, wheels or tools. Wait for driver capacitors to discharge (time TBD from driver datasheet). Lift robot onto stands for wheel-free tests.

See also `FMEA.md` and `RISK_REGISTER.md`.
