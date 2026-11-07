# Firmware
`firmware/motor_controller` — PlatformIO (ESP32, Arduino framework). Skeleton: serial command `V <left_rad_s> <right_rad_s>`, command watchdog (stops motors after `CMD_TIMEOUT_MS`), E-stop sense. Motor control loop / PID tuning: TBD. micro-ROS vs. serial bridge: decision TBD.
Build: `pio run`. Not yet flashed to hardware.
