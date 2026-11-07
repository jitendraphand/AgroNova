// AgroNova motor controller r0.2 — closed-loop wheel speed control. NOT validated on hardware.
// Pin map must match docs/electronics/WIRING.md. 4 motors are driven as 2 sides (left pair / right pair
// share a driver channel each); one encoder per side is used for feedback (A-23).
#include <Arduino.h>
#include "pid.h"

static const int L_PWM = 25, L_DIR = 26, R_PWM = 32, R_DIR = 33;
static const int L_ENC_A = 34, L_ENC_B = 35, R_ENC_A = 36, R_ENC_B = 39;
static const int ESTOP_SENSE = 27;            // HIGH = safety chain closed (motor power enabled)
static const uint32_t CMD_TIMEOUT_MS = 500;   // R-005
static const uint32_t LOOP_MS = 10;           // 100 Hz control loop
static const float MAX_WHEEL_RAD_S = 7.0f;    // ~1.0 m/s / 0.15 m (R-008)
// Encoder counts per WHEEL revolution = encoder CPR x 4 (quadrature) x gear ratio. TBD from motor datasheet;
// placeholder value must be replaced and verified by calibration procedure CAL-002.
static const float COUNTS_PER_WHEEL_REV = 4.0f * 11.0f * 90.0f;
// Gains are UNTUNED starting values (see docs/firmware/README.md tuning procedure).
static Pid pid_l(0.08f, 0.6f, 0.0f, -1.0f, 1.0f), pid_r(0.08f, 0.6f, 0.0f, -1.0f, 1.0f);

static volatile int32_t enc_l = 0, enc_r = 0;
static float target_l = 0, target_r = 0;
static uint32_t last_cmd_ms = 0, last_loop_ms = 0;
static int32_t prev_l = 0, prev_r = 0;

void IRAM_ATTR isrL() { enc_l += (digitalRead(L_ENC_A) == digitalRead(L_ENC_B)) ? 1 : -1; }
void IRAM_ATTR isrR() { enc_r += (digitalRead(R_ENC_A) == digitalRead(R_ENC_B)) ? -1 : 1; }  // mirrored side

static void drive(int pwmPin, int dirPin, float duty) {
  duty = constrain(duty, -1.0f, 1.0f);
  digitalWrite(dirPin, duty >= 0 ? HIGH : LOW);
  ledcWrite(pwmPin, (uint32_t)(fabsf(duty) * 1023));
}

static void stopAll() {
  ledcWrite(L_PWM, 0); ledcWrite(R_PWM, 0);
  target_l = target_r = 0; pid_l.reset(); pid_r.reset();
}

void setup() {
  Serial.begin(115200);
  pinMode(L_DIR, OUTPUT); pinMode(R_DIR, OUTPUT); pinMode(ESTOP_SENSE, INPUT);
  pinMode(L_ENC_A, INPUT); pinMode(L_ENC_B, INPUT); pinMode(R_ENC_A, INPUT); pinMode(R_ENC_B, INPUT);
  attachInterrupt(digitalPinToInterrupt(L_ENC_A), isrL, CHANGE);
  attachInterrupt(digitalPinToInterrupt(R_ENC_A), isrR, CHANGE);
  ledcAttach(L_PWM, 20000, 10);
  ledcAttach(R_PWM, 20000, 10);
  stopAll();  // safe startup: motors off until a valid command arrives
}

void loop() {
  // Command: "V <left_rad_s> <right_rad_s>\n"   Feedback: "S <left_rad_s> <right_rad_s> <estop_ok>\n"
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    float l, r;
    if (sscanf(line.c_str(), "V %f %f", &l, &r) == 2) {
      target_l = constrain(l, -MAX_WHEEL_RAD_S, MAX_WHEEL_RAD_S);
      target_r = constrain(r, -MAX_WHEEL_RAD_S, MAX_WHEEL_RAD_S);
      last_cmd_ms = millis();
    }
  }
  uint32_t now = millis();
  if (now - last_loop_ms < LOOP_MS) return;
  float dt = (now - last_loop_ms) * 1e-3f;
  last_loop_ms = now;

  noInterrupts(); int32_t cl = enc_l, cr = enc_r; interrupts();
  float w_l = (cl - prev_l) / COUNTS_PER_WHEEL_REV * 2.0f * PI / dt;
  float w_r = (cr - prev_r) / COUNTS_PER_WHEEL_REV * 2.0f * PI / dt;
  prev_l = cl; prev_r = cr;

  bool estop_ok = digitalRead(ESTOP_SENSE) == HIGH;
  // Watchdog: comms loss or open safety chain -> stop. Hardware chain removes motor power independently.
  if (!estop_ok || now - last_cmd_ms > CMD_TIMEOUT_MS) {
    stopAll();
  } else {
    drive(L_PWM, L_DIR, pid_l.update(target_l, w_l, dt));
    drive(R_PWM, R_DIR, pid_r.update(target_r, w_r, dt));
  }
  Serial.printf("S %.3f %.3f %d\n", w_l, w_r, estop_ok ? 1 : 0);
}
