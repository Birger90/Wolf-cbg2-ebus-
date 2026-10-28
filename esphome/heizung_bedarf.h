#pragma once
#include <cmath>
#include <cstdint>
#include <cstring>

// Zwei 16-Bit-Modbus-Registerwerte (als float aus ESPHome-Sensoren) zu einem IEEE-754-Float zusammensetzen.
// hi = höherwertiges Wort, lo = niederwertiges Wort. NAN, wenn eines der Register noch nicht gelesen wurde.
static inline float fp32_from(float hi, float lo) {
  if (std::isnan(hi) || std::isnan(lo)) return NAN;
  uint32_t u = (static_cast<uint32_t>(static_cast<uint16_t>(hi)) << 16) | static_cast<uint16_t>(lo);
  float v;
  std::memcpy(&v, &u, sizeof(v));
  return v;
}
