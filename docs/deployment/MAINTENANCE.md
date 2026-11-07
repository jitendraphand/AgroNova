# Maintenance & troubleshooting (r0.2)
Intervals are initial proposals (no field data yet); revise from operating logs.

## Preventive maintenance
| Interval | Task |
|---|---|
| Before every run | Clean lidar window & camera; test ES1/ES2 (TC-SAF-001 quick); check tyre pressure/damage; battery SOC |
| Weekly / 20 h | Retorque wheel and motor-mount bolts (torque TBD per fastener); inspect cables & glands; clean mud from wheel wells |
| Monthly / 80 h | Inspect printed parts for cracks/creep (INS-020); check enclosure seals; inspect contactor operation count |
| Season end | Store battery at ~50 % SOC in shade; full inspection; replace worn tyres |

## Troubleshooting
| Symptom | Likely causes | Diagnosis | Fix | Prevention |
|---|---|---|---|---|
| Robot not powering on | SW1 off, F1/F2 blown, BMS cut-off | DMM at battery, after F1, after SW1 | Replace fuse after finding short; charge battery | Pre-run checklist |
| Motors don't respond, Pi OK | K1 open (E-stop pressed / not RESET), F3/F4, watchdog | Check `S ... 0` estop flag; 24 V at driver | Release E-stops, press RESET | — |
| Wrong motor direction | Leads swapped | CAL-004 | Swap leads or DIR logic | Label leads |
| Odometry drifts | Wrong r or b_eff, wheel slip | CAL-001/003 | Recalibrate on site soil | Fuse IMU in EKF |
| Encoder reads 0 | Cable, level shifter, wrong pins | Rotate wheel by hand, watch count | Repair cable | Shielded cable, strain relief |
| ROS 2 nodes can't see each other | ROS_DOMAIN_ID mismatch, firewall, Wi-Fi | `ros2 topic list` on both | Same domain ID; check network | Document network config |
| GNSS no fix / jumps | Antenna blocked, no RTK | `ros2 topic echo /gps/fix` status | Relocate antenna; check NTRIP | — |
| Motor overheats | Stall in mud, overload | Current & temp log | Reduce load/speed | Stall detection (TBD) |
| Battery voltage sags | Ageing cells, high current | Voltage under load | Replace battery | Avoid deep discharge |
| Printed part cracks | Wrong material, orientation | Inspect fracture | Reprint per print sheet (ASA) | Monthly inspection |
