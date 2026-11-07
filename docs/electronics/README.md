# Electronics
Status: NOT STARTED. Baseline: 24 V LiFePO4 → main fuse → hardware E-stop contactor → motor drivers; DC-DC 5 V for Pi 5, 3.3 V for ESP32.
Deliverables pending: KiCad schematic/PCB (`hardware/pcb/`), pin map, wire-gauge & fuse calculations, grounding/EMC plan. All component models **TBD** — no datasheet values are claimed.

## Pin map (firmware placeholder — must match final schematic)
| Signal | ESP32 GPIO |
|---|---|
| Left PWM / DIR | 25 / 26 |
| Right PWM / DIR | 32 / 33 |
| Left encoder A/B | 34 / 35 |
| Right encoder A/B | 36 / 39 |
| E-stop sense (input only) | 27 |
