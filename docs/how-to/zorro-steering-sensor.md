---
title: Zorro Steering Sensor (ZSS)
---

# Zorro Steering Sensor (ZSS)

## What It Is

The Zorro Steering Sensor is an aftermarket steering angle sensor for Toyota and Lexus vehicles. It provides a higher-resolution steering angle measurement than the factory sensor, which can improve lateral control accuracy.

## How sunnypilot Uses It

When a Zorro Steering Sensor is detected, sunnypilot reads the steering angle from the `SECONDARY_STEER_ANGLE` CAN message (`ZORRO_STEER` signal) instead of relying solely on the factory sensor.

### Offset Calibration

The Zorro Steering Sensor has a different zero point than the factory sensor. sunnypilot automatically calibrates the offset:

1. When cruise control becomes available, the offset calculation is triggered
2. sunnypilot computes the difference between the ZSS reading and the factory steering angle
3. This offset is applied to all subsequent ZSS readings

### Safety Checks

To prevent using bad data, sunnypilot applies a sanity check:

- If the ZSS-corrected angle differs from the factory angle by more than 4 degrees, a threshold counter increments
- After 10 consecutive threshold violations, the ZSS reading is rejected and the factory angle is used instead
- This protects against sensor faults or calibration drift

## Requirements

!!! info "Requirements"
    - Zorro Steering Sensor hardware installed on a Toyota or Lexus vehicle
    - The sensor must be properly wired to the CAN bus

## Credits

Zorro Steering Sensor support was developed with contributions from zorrobyte, ErichMoraga, and dragonpilot.

## Related

- [Toyota / Lexus Settings](../settings/vehicle/toyota.md)
- [Torque Control](../features/steering/torque-control.md)
