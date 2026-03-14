---
title: Chrysler / Dodge / Jeep / RAM Settings
---

# Chrysler / Dodge / Jeep / RAM Vehicle Settings

Information about sunnypilot behavior on Chrysler, Dodge, Jeep, and RAM vehicles. These notes apply when one of these vehicles is connected or selected.

**Location**: `Settings -> Vehicle`

---

## MADS via LKAS Button

On Chrysler, Dodge, Jeep, and RAM vehicles, [MADS](../../features/steering/mads.md) is toggled using the LKAS button on the steering wheel. Press the LKAS button to enable or disable steering assistance independently of cruise control.

- **Non-RAM vehicles**: The LKAS state is tracked through the LKAS heartbeat message
- **RAM vehicles**: The LKAS state is read from the Center Stack button

---

## ICBM Support

[Intelligent Cruise Button Management (ICBM)](../../features/cruise/icbm.md) is supported on Chrysler, Dodge, Jeep, and RAM vehicles. The button simulation approach differs by platform:

- **RAM vehicles**: Uses direct cruise button commands
- **Non-RAM vehicles**: Uses a counter-offset cycling pattern for button simulation

---

## Steer to Zero

Some Chrysler/Dodge/Jeep/RAM vehicles support steering assistance down to 0 mph (no minimum steering speed requirement). On supported vehicles, sunnypilot can provide lateral control at any speed, including during stop-and-go traffic.

---

## RAM-Specific Notes

- **RAM HD**: Uses a direct steering angle source for improved accuracy
- **RAM DT**: Includes a smooth ramp-in for LKAS control at the minimum enable speed to prevent abrupt steering engagement
