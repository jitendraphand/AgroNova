# FMEA (r0.2, design FMEA draft). S/O/D 1–10, RPN = S×O×D. Ratings are engineering estimates, to be reviewed.
| ID | Item | Failure mode | Effect | Cause | S | O | D | RPN | Mitigation | Owner/Status |
|---|---|---|---|---|---|---|---|---|---|---|
| FM-01 | K1 contactor | Contacts weld closed | E-stop does not cut motors | Inrush/overcurrent | 10 | 3 | 6 | 180 | Monitored safety relay K2, contactor rated ≥ 2× peak, periodic E-stop test | Open |
| FM-02 | E-stop wiring | Wire breaks | Robot stops (fail-safe) | Vibration | 3 | 4 | 2 | 24 | NC chain is fail-safe; strain relief | Open |
| FM-03 | Encoder | Signal loss | Wrong speed, PID saturates → runaway | Cable damage, mud | 8 | 4 | 5 | 160 | Firmware plausibility check (TBD: duty>0.5 & speed≈0 → fault stop), shielded cable | Open |
| FM-04 | Serial link | Pi–ESP32 link drops | Last command held | USB unplug, Pi crash | 8 | 3 | 2 | 48 | 500 ms watchdog (implemented) | Implemented, untested |
| FM-05 | Battery | Thermal runaway / overheating | Fire | Cell damage, 45 °C sun | 10 | 2 | 5 | 100 | LiFePO4, BMS with temp cutoff, ventilated shaded box | Open |
| FM-06 | Printed covers | Creep / UV cracking | Water ingress | PLA used, UV | 5 | 4 | 4 | 80 | ASA only, inspection INS-020 | Open |
| FM-07 | GNSS | Position jump/loss | Leaves row, crop damage | Tree cover, multipath | 6 | 5 | 4 | 120 | EKF covariance gating, lidar row following (TBD), geofence | Open |
| FM-08 | Motor | Overheat | Loss of drive | Mud stall, slope | 5 | 4 | 4 | 80 | Driver current limit, stall detection (TBD), thermal test TC-ELEC-005 | Open |
| FM-09 | Enclosure | Water ingress (monsoon) | Short circuit | Seal failure | 7 | 4 | 4 | 112 | IP65 commercial box, glands, spray test TC-ENV-001 | Open |
| FM-10 | Lidar | Mud on window | Obstacle not detected | Field soil | 9 | 5 | 6 | 270 | Pre-run cleaning checklist, self-check of scan validity (TBD), low speed | Open — highest RPN |
