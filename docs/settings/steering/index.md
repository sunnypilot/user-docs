---
title: Steering Settings
---

# Steering Settings

Configure lateral (steering) control behavior including MADS, lane changes, blinker pause, and torque tuning.

**Location**: `Settings -> Steering`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Modular Assistive Driving System (MADS)

A toggle that enables MADS, which decouples lateral (steering) control from longitudinal (speed) control. With MADS on, steering assistance can remain active even when cruise control is not engaged.

Turn this toggle **on** to enable MADS, or **off** to revert to standard engagement behavior.

When enabled, a **Customize MADS** button appears below the toggle. Tap it to open the [MADS sub-panel](mads.md) where you can configure engagement modes and brake pedal behavior.

!!! note "Platform-specific behavior"
    Some vehicles (Rivian, certain Tesla configurations) show limited MADS settings. The system displays a note indicating which options are restricted for your vehicle.

---

## Customize Lane Change

A button that opens the [Lane Change sub-panel](lane-change.md) where you can set the auto lane change timer and blind spot monitoring delay.

---

## Pause Lateral Control with Blinker

When you activate your turn signal, this feature temporarily pauses automatic steering so you can take manual control of the wheel. Useful during merges, parking, or any situation where you want to steer by hand while keeping the system otherwise active.

Turn this toggle **on** to enable it.

### Minimum Speed to Pause Lateral Control

Once the blinker pause toggle is enabled, a speed selector appears directly below it. Use the **-** and **+** buttons to set the speed threshold. Lateral control only pauses when your current speed is below this value while the blinker is on. The speed displays in your preferred unit (km/h or mph).

### Post-Blinker Delay

A second selector lets you choose how many seconds the system waits after the blinker turns off before resuming automatic steering. The delay ranges from 0 to 10 seconds.

!!! tip
    Set the delay to at least 1-2 seconds to avoid the system resuming steering while you are still mid-maneuver.

---

## Enforce Torque Lateral Control

Forces torque-based lateral control on your vehicle, even if it does not use torque control by default.

When enabled, a **Customize Torque Params** button appears below the toggle. Tap it to open the [Torque sub-panel](torque.md) for advanced tuning.

!!! note "Availability"
    This toggle is hidden on vehicles with angle-based steering. Enabling this disables Neural Network Lateral Control (NNLC), and vice versa. The device must be offroad (parked, ignition off) to change this setting.

---

## Neural Network Lateral Control (NNLC)

Enables a neural network model to handle lateral control instead of the traditional controller. NNLC can provide smoother steering in some situations.

!!! note "Availability"
    This toggle is hidden on vehicles with angle-based steering. Enabling this disables Enforce Torque Lateral Control, and vice versa. The device must be offroad to change this setting.

---

## Sub-Panels

The Steering section contains these additional configuration pages:

- **[MADS Settings](mads.md)** - configure engagement modes and brake pedal behavior
- **[Lane Change Settings](lane-change.md)** - configure auto lane change timing and blind spot monitoring
- **[Torque Settings](torque.md)** - fine-tune torque lateral control parameters

---

## Related Features

- [Modular Assistive Driving System](../../features/steering/mads.md)
- [Neural Network Lateral Control](../../features/steering/nnlc.md)
- [Auto Lane Change](../../features/steering/auto-lane-change.md)
- [Torque Control](../../features/steering/torque-control.md)
