# Wiring & power distribution (r0.2 — design draft, not built)

## Power distribution diagram
```
 [BAT1 25.6 V 8S LiFePO4 ≥ 25 Ah, with BMS]  (AN-ELEC-001)
   │ +   (6 mm² red, W01)
   ▼
 [F1 main fuse 30 A, ANL/MIDI type, ≤ 150 mm from battery]  (AN-ELEC-010)
   │
 [SW1 main isolator, 50 A DC rated]  (AN-ELEC-011)
   ├────────────────────────────────────────────┐
   │ (6 mm², W02)                               │ (1.5 mm², W10)
 [K1 motor contactor NO, coil 24 V] ◄── safety chain (below)   [F2 5 A] → [DC-DC 24→5 V ≥ 5 A] → Pi 5 (USB-C/GPIO 5 V)
   │ (6 mm²)                                    │                         → [5→3.3 V on ESP32 board]
 [F3 20 A]──[MD1 driver L]──M1,M2 (left pair)   └─[F4 2 A] → sensors 12 V via DC-DC (lidar/GNSS as required)
 [F4 20 A]──[MD2 driver R]──M3,M4 (right pair)
   │
 BAT− ─ (6 mm² black) ─ star ground bus GND1 ─ driver GND, DC-DC GND, chassis bond via 1 point (A-24)
```
Wire sizes follow `docs/calculations/RESULTS.md` (peak ≈ 17 A; 6 mm² gives 0.6 % drop). Fuse ratings are draft: F1 ≥ 1.25 × peak → 30 A standard value. Verify against cable ampacity datasheet.

Protections: BMS (over/under-voltage, over-current, temperature — from battery datasheet, TBD), reverse polarity: keyed Anderson SB50 battery connector + main fuse (A-25), TVS across 24 V bus near drivers (part TBD).

## Safety chain (hardware E-stop) — see docs/safety/SAFETY.md
```
 +24V ─[F5 1 A]─[ES1 mushroom NC]─[ES2 rear NC]─[RX1 wireless E-stop relay NC]─[K2 safety relay / monitored]─ K1 coil ─ GND
                                                                                   │
                                                          ESP32 GPIO27 ← opto-isolated sense of K1 coil voltage
```
Opening any NC contact de-energises K1 → motor drivers lose power. Software cannot re-close it; reset requires pressing RESET (S2) after all E-stops released (K2 latching, A-26).

## Signal connections (ESP32 DevKitC)
| Wire | From | To | Signal | Gauge |
|---|---|---|---|---|
| S01/S02 | GPIO25 / GPIO26 | MD1 PWM / DIR | Left drive | 0.5 mm² |
| S03/S04 | GPIO32 / GPIO33 | MD2 PWM / DIR | Right drive | 0.5 mm² |
| S05/S06 | GPIO34 / GPIO35 | Left encoder A/B (via 5→3.3 V level shift if encoder is 5 V) | | shielded 4-core |
| S07/S08 | GPIO36 / GPIO39 | Right encoder A/B | | shielded 4-core |
| S09 | GPIO27 | Opto output (K1 sense) | E-stop status | 0.5 mm² |
| S10 | USB | Pi 5 USB | Serial 115200 | USB cable |

Labelling: every wire carries heat-shrink label `<WireID>` matching this table. Connectors: Deutsch DT or IP67 M12 for external runs (A-27), JST-XH inside enclosure.

## Grounding & EMC
Single-point star ground; motor leads twisted pairs; encoder cables shielded, shield grounded at controller end only; 20 kHz PWM (above audible); ferrites on motor leads (TBD after EMC pre-scan).

## Open
KiCad schematic + interface PCB (`hardware/pcb/`), connector pinouts per part, thermal check of drivers in sealed enclosure at 45 °C ambient.
