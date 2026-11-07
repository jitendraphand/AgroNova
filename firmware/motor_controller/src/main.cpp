// AgroNova motor controller — SKELETON. Not validated on hardware.
// Pin map must match docs/electronics/README.md and the final schematic (TBD).
#include <Arduino.h>

static const int L_PWM = 25, L_DIR = 26, R_PWM = 32, R_DIR = 33;
static const int ESTOP_SENSE = 27;            // HIGH = E-stop chain closed (OK)
static const uint32_t CMD_TIMEOUT_MS = 500;   // R-005 (value TBD)
static const float MAX_WHEEL_RAD_S = 10.0f;   // TBD from motor selection

static uint32_t last_cmd_ms = 0;

static void setMotor(int pwmPin, int dirPin, float w) {
  float duty = constrain(fabsf(w) / MAX_WHEEL_RAD_S, 0.0f, 1.0f);
  digitalWrite(dirPin, w >= 0 ? HIGH : LOW);
  ledcWrite(pwmPin, (uint32_t)(duty * 1023));  // open loop; PID TBD
}

static void stopAll() { ledcWrite(L_PWM, 0); ledcWrite(R_PWM, 0); }

void setup() {
  Serial.begin(115200);
  pinMode(L_DIR, OUTPUT); pinMode(R_DIR, OUTPUT); pinMode(ESTOP_SENSE, INPUT);
  ledcAttach(L_PWM, 20000, 10);  // Arduino-ESP32 core 3.x API
  ledcAttach(R_PWM, 20000, 10);
  stopAll();
}

void loop() {
  // Protocol: "V <left_rad_s> <right_rad_s>\n"
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    float l, r;
    if (sscanf(line.c_str(), "V %f %f", &l, &r) == 2) {
      if (digitalRead(ESTOP_SENSE) == HIGH) { setMotor(L_PWM, L_DIR, l); setMotor(R_PWM, R_DIR, r); }
      last_cmd_ms = millis();
    }
  }
  // Software watchdog. NOTE: hardware E-stop removes motor power independently.
  if (millis() - last_cmd_ms > CMD_TIMEOUT_MS || digitalRead(ESTOP_SENSE) == LOW) stopAll();
}
