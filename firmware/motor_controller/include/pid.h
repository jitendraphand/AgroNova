// AgroNova discrete PID with output clamp and conditional-integration anti-windup.
// Header-only, no Arduino dependency, so it can be unit-tested on a host (test_host/).
#pragma once

struct Pid {
  float kp, ki, kd, out_min, out_max;
  float integ = 0.0f, prev_err = 0.0f;
  bool first = true;

  Pid(float p, float i, float d, float lo, float hi) : kp(p), ki(i), kd(d), out_min(lo), out_max(hi) {}

  void reset() { integ = 0.0f; prev_err = 0.0f; first = true; }

  float update(float setpoint, float measured, float dt) {
    if (dt <= 0.0f) return 0.0f;
    float err = setpoint - measured;
    float deriv = first ? 0.0f : (err - prev_err) / dt;
    first = false;
    prev_err = err;
    float candidate_integ = integ + err * dt;
    float out = kp * err + ki * candidate_integ + kd * deriv;
    if (out > out_max) {
      out = out_max;  // do not integrate further into saturation
      if (err < 0) integ = candidate_integ;
    } else if (out < out_min) {
      out = out_min;
      if (err > 0) integ = candidate_integ;
    } else {
      integ = candidate_integ;
    }
    return out;
  }
};
