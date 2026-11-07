// Host unit test: closed-loop PID on a first-order motor model (simulation only, not hardware).
#include <cassert>
#include <cmath>
#include <cstdio>
#include "../include/pid.h"

int main() {
  // Plant: dw/dt = (K*u - w)/tau, K=12 rad/s per unit duty, tau=0.15 s (ASSUMED model)
  Pid pid(0.08f, 0.6f, 0.0f, -1.0f, 1.0f);
  float w = 0.0f, dt = 0.005f;
  for (int k = 0; k < 600; ++k) {
    float u = pid.update(6.0f, w, dt);
    assert(u <= 1.0f && u >= -1.0f);
    w += (12.0f * u - w) / 0.15f * dt;
  }
  std::printf("final speed %.3f rad/s (target 6.0)\n", w);
  assert(std::fabs(w - 6.0f) < 0.05f);
  // Saturation / anti-windup: unreachable setpoint must not blow up the integrator
  Pid sat(0.1f, 1.0f, 0.0f, -1.0f, 1.0f);
  for (int k = 0; k < 10000; ++k) sat.update(100.0f, 0.0f, 0.01f);
  assert(sat.integ < 20.0f);
  assert(sat.update(0.0f, 0.0f, 0.01f) <= 1.0f);
  Pid z(1, 1, 1, -1, 1);
  assert(z.update(1, 0, 0) == 0.0f);
  std::puts("PID host tests passed");
  return 0;
}
