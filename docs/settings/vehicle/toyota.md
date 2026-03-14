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

When enabled, sunnypilot does not control gas or brakes. The factory Toyota/Lexus adaptive cruise control system handles all speed control. sunnypilot still provides steering assistance.

Enabling this will disable sunnypilot longitudinal control, disable Alpha Longitudinal if it was enabled, and force Stop and Go Hack off. A confirmation dialog appears before activation.

!!! note "Availability"
    Cannot be changed while the system is engaged (actively driving).

---

## Stop and Go Hack (Alpha)

Allows some Toyota and Lexus vehicles to automatically resume from a full stop during stop-and-go traffic. Without this, you must press the resume button or tap the gas to resume.

!!! warning "Alpha Feature"
    This is an alpha-quality feature. Use at your own risk.

!!! note "Availability"
    Requires sunnypilot longitudinal control to be available and enabled. **Enforce Factory Longitudinal Control** must be off. Cannot be changed while engaged.

---

## Zorro Steering Sensor (ZSS)

Toyota and Lexus vehicles with a Zorro Steering Sensor installed gain higher-resolution steering angle measurements. sunnypilot automatically detects the ZSS, calibrates the offset, and uses the improved angle data for lateral control.

See the [Zorro Steering Sensor (ZSS)](../../how-to/zorro-steering-sensor.md) guide for details.

---

## Gas Interceptor (comma Pedal)

Toyota and Lexus vehicles with a Gas Interceptor (commonly known as comma Pedal) installed gain longitudinal control through sunnypilot. The gas command scaling is tuned per vehicle model for optimal response.

See the [Gas Interceptor (comma Pedal)](../../how-to/gas-interceptor.md) guide for details.

---

## Traffic Signal Recognition (RSA)

Some Toyota and Lexus vehicles broadcast speed limit data via RSA (Road Sign Assist) CAN messages. sunnypilot reads RSA1 and RSA2 messages to extract speed limits in both kph and mph formats. This data is used by [Speed Limit Assist](../../features/cruise/speed-limit.md) when available.

---

## Smart DSU

Toyota and Lexus TSS 1.0 vehicles with an aftermarket Smart DSU module can gain longitudinal control override. When a Smart DSU is detected, sunnypilot adjusts its ACC interface accordingly.
