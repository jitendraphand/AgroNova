# Firmware (r0.2)
`firmware/motor_controller` — PlatformIO, ESP32 (`espressif32 @ 8.0.0`, Arduino core 3.x).

| Feature | Status |
|---|---|
| Serial protocol `V <l> <r>` → `S <l> <r> <estop_ok>` @100 Hz | Implemented, builds |
| Quadrature encoders (interrupt, 1 per side) | Implemented, builds; COUNTS_PER_WHEEL_REV placeholder |
| PID speed loop (`include/pid.h`, anti-windup) | Implemented; host unit test on an ASSUMED motor model passes |
| Comms-loss watchdog 500 ms, E-stop sense, safe startup | Implemented, not bench-tested |
| micro-ROS | Not started (serial bridge node also TBD) |

Build: `pio run`. Host test: `pytest tests/test_firmware_host.py`.

## PID tuning procedure (hardware, TBD results)
1. Robot on stands, wheels free; E-stop within reach.
2. Set ki=kd=0; raise kp until step response 0→3 rad/s oscillates; use 50 % of that kp.
3. Raise ki until steady-state error < 2 % within 1 s, overshoot < 15 %.
4. Repeat on ground in field soil; record in a test record (TC-FW-003). Update gains in `main.cpp`.
