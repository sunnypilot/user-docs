---
title: Toyota / Lexus Settings
---

# Toyota / Lexus Vehicle Settings

Settings specific to Toyota and Lexus vehicles. These appear in the Vehicle panel when a Toyota or Lexus vehicle is connected or selected.

**Location**: `Settings -> Vehicle`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Enforce Factory Longitudinal Control

When enabled, sunnypilot does not control acceleration or braking. The factory Toyota/Lexus adaptive cruise control system handles all speed control. sunnypilot still provides steering assistance.

Enabling this will disable sunnypilot longitudinal control, disable Alpha Longitudinal if it was enabled, and force Stop and Go Hack off. A confirmation dialog appears before activation.

!!! note "Availability"
    Cannot be changed while the system is engaged (actively driving).

---

## Stop and Go Hack (Alpha)

Allows some Toyota and Lexus vehicles to automatically resume from a full stop during stop-and-go traffic. Without this, you must press the resume button or tap the accelerator to resume.

!!! warning "Alpha Feature"
    This is an alpha-quality feature. Use at your own risk.

!!! note "Availability"
    Requires sunnypilot longitudinal control to be available and enabled. **Enforce Factory Longitudinal Control** must be off. Cannot be changed while engaged.

---

## Zorro Steering Sensor (ZSS)

Toyota and Lexus vehicles with a Zorro Steering Sensor installed gain higher-resolution steering angle measurements. sunnypilot automatically detects the ZSS when the hardware broadcasts on the CAN bus — no user configuration is needed.

!!! warning "SecOC Exclusion"
    ZSS is not compatible with SecOC-equipped Toyota/Lexus vehicles (newer models with secure CAN authentication). These vehicles are automatically excluded during fingerprinting.

See the [Zorro Steering Sensor (ZSS)](../../how-to/zorro-steering-sensor.md) guide for details.

---

## Gas Interceptor (comma Pedal)

Toyota and Lexus vehicles with a Gas Interceptor (commonly known as comma Pedal) installed gain longitudinal control through sunnypilot. The accelerator command scaling is tuned per vehicle model for optimal response.

All three conditions must be met for the Gas Interceptor to be enabled:

1. Gas Interceptor hardware installed and detected on the CAN bus
2. [Alpha Longitudinal](../../features/cruise/alpha-longitudinal.md) enabled in **Settings -> Developer -> sunnypilot Longitudinal Control (Alpha)** — this sets `openpilotLongitudinalControl` to true, which the Gas Interceptor requires
3. Vehicle is not SecOC-equipped (newer models with secure CAN authentication)

When the Gas Interceptor hardware is detected, sunnypilot sets `alphaLongitudinalAvailable` to true, making the Alpha Longitudinal toggle visible in Developer settings. The user must then manually enable it for the Gas Interceptor to function.

When enabled, the Gas Interceptor also enables stop-and-go capability (automatic resume from a full stop).

See the [Gas Interceptor (comma Pedal)](../../how-to/gas-interceptor.md) guide for details.

---

## Traffic Signal Recognition (RSA)

sunnypilot always attempts to read RSA (Road Sign Assist) CAN messages on all Toyota and Lexus vehicles — no toggle or configuration is needed. RSA1 and RSA2 messages are read to extract speed limits in both kph and mph formats. If your vehicle's camera broadcasts RSA messages, the speed limit data appears automatically and is used by [Speed Limit Assist](../../features/cruise/speed-limit.md). If RSA messages are not present, this is silently skipped.

---

## Smart DSU

Toyota and Lexus TSS 1.0 vehicles with an aftermarket Smart DSU module can gain longitudinal control override. The Smart DSU is automatically detected during fingerprinting when the device is present on the CAN bus — no user configuration is needed.

When detected, the Smart DSU sets `alphaLongitudinalAvailable` to true, which makes the [Alpha Longitudinal](../../features/cruise/alpha-longitudinal.md) toggle visible in **Settings -> Developer**. The user must then manually enable Alpha Longitudinal for the Smart DSU to provide longitudinal control and stop-and-go capability.
