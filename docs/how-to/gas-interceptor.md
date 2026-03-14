---
title: Gas Interceptor (comma Pedal)
---

# Gas Interceptor (comma Pedal)

## What It Is

The Gas Interceptor (commonly known as comma Pedal) is an aftermarket hardware device that sits between the accelerator pedal and the vehicle's ECU. It allows sunnypilot to send gas commands, enabling longitudinal (speed) control on vehicles that don't support it through the stock CAN bus.

## Supported Vehicles

### Toyota / Lexus

The Gas Interceptor enables sunnypilot longitudinal control on Toyota and Lexus vehicles that lack factory support for direct throttle control.

!!! info "Prerequisites (all three required)"
    - Gas Interceptor hardware installed and detected on the CAN bus
    - [Alpha Longitudinal](../features/cruise/alpha-longitudinal.md) enabled in **Settings -> Developer -> sunnypilot Longitudinal Control (Alpha)** — when the Gas Interceptor is detected, `alphaLongitudinalAvailable` is set to true, making this toggle visible. The user must manually enable it to activate `openpilotLongitudinalControl`.
    - Vehicle is **not** SecOC-equipped (newer models with secure CAN authentication are excluded)

When all prerequisites are met, the Gas Interceptor also enables stop-and-go capability (automatic resume from a full stop).

The gas command scaling is tuned per vehicle:

| Vehicle | Pedal Sensitivity | Notes |
|---------|------------------|-------|
| RAV4, RAV4 Hybrid, Highlander | Conservative (0.15-0.3) | These models have a more sensitive gas pedal |
| Corolla | Moderate (0.3-0.4) | |
| Other Toyota/Lexus | Standard (0.4-0.5) | Default scaling for all other models |

The maximum gas command is capped at 0.3 for safety. Wind brake compensation is applied at higher speeds to maintain smooth control.

### Honda / Acura

Honda and Acura vehicles use a speed-dependent gas multiplier — 0.4x at standstill, linearly increasing to 1.0x at approximately 10 m/s (22 mph). This provides gentler acceleration from stops while maintaining full responsiveness at driving speeds. Wind brake compensation is also applied.

!!! info "Platform Restriction"
    The Gas Interceptor is only supported on non-Bosch Honda/Acura platforms. Bosch-equipped vehicles skip Gas Interceptor detection entirely.

## How sunnypilot Uses It

1. sunnypilot calculates the desired acceleration based on the driving model and lead vehicle
2. The acceleration value is converted to a pedal command using vehicle-specific scaling
3. A speed-dependent offset compensates for engine creep and wind resistance
4. The pedal command is clipped to the maximum safe value and sent to the Gas Interceptor over CAN
5. The Gas Interceptor applies the greater of the driver's physical pedal input or sunnypilot's command

!!! info "Driver Override"
    The Gas Interceptor always respects the driver's physical pedal input. If you press the gas pedal harder than sunnypilot's command, your input takes priority.

## Requirements

!!! info "Requirements"
    - Gas Interceptor hardware installed and wired to the comma device
    - A compatible Toyota/Lexus or Honda/Acura vehicle
    - **Toyota/Lexus**: [Alpha Longitudinal](../features/cruise/alpha-longitudinal.md) must be enabled in **Settings -> Developer** — the Gas Interceptor hardware makes this toggle available, but the user must enable it manually

## Related

- [Alpha Longitudinal](../features/cruise/alpha-longitudinal.md) — Longitudinal control settings
- [Toyota / Lexus Settings](../settings/vehicle/toyota.md)
- [Honda / Acura Settings](../settings/vehicle/honda.md)
