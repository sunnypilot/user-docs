---
title: Cruise Control Settings
---

# Cruise Control Settings

Configure adaptive cruise control behavior, including intelligent button management, smart cruise features, and custom speed increments.

**Location**: `Settings -> Cruise`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Intelligent Cruise Button Management (ICBM) (Alpha)

Allows sunnypilot to dynamically manage cruise speed by intercepting button presses on the steering wheel. When enabled, speed adjustments are handled intelligently to support features like Speed Limit Assist.

!!! note "Vehicle Compatibility"
    This toggle only appears if your vehicle supports ICBM. If you do not see it, your vehicle does not support this feature.

---

## Smart Cruise Control - Vision

Uses vision-based path predictions to estimate the appropriate speed to drive through turns ahead. The system monitors predicted lateral acceleration and smoothly decelerates when entering curves, then accelerates back to your set speed when exiting.

!!! note "Availability"
    Requires longitudinal control, or ICBM must be enabled.

---

## Smart Cruise Control - Map

Uses map data to estimate the appropriate speed to drive through turns ahead. The system calculates deceleration distance based on your current speed and upcoming waypoint target velocities.

!!! note "Availability"
    Requires longitudinal control, or ICBM must be enabled.

---

## Custom ACC Speed Increments

Enables customization of how much the set speed changes with short and long button presses on the steering wheel.

!!! note "Availability"
    Requires longitudinal control (or ICBM enabled), and PCM Cruise must not be active.

### Short Press Increment

Once the toggle is enabled, a selector appears below it. Use the **-** and **+** buttons to set the speed change (in km/h or mph) for a short press of the cruise speed button. The range is 1 to 10.

### Long Press Increment

A second selector lets you choose the speed change for a long press:

| Selection | Speed change |
|-----------|-------------|
| **1** | 1 km/h (or mph) |
| **2** | 5 km/h (or mph) |
| **3** | 10 km/h (or mph) |

---

## Enable Dynamic Experimental Control

Automatically switches between standard and experimental driving mode based on driving conditions. When enabled, the system uses real-time signals (speed, turn detection, stop signs, traffic lights) to determine the most appropriate mode.

!!! note "Availability"
    Requires longitudinal control. The device must be offroad (parked, ignition off) to change this setting.

---

## Speed Limit

A button that opens the [Speed Limit sub-panel](speed-limit/index.md) where you can configure speed limit mode, offset, and data source.

---

## Related Features

- [Intelligent Cruise Button Management](../../features/cruise/icbm.md)
- [Smart Cruise Control - Vision](../../features/cruise/scc-v.md)
- [Smart Cruise Control - Map](../../features/cruise/scc-m.md)
- [Custom ACC Increments](../../features/cruise/custom-acc-increments.md)
- [Dynamic Experimental Control](../../features/cruise/dynamic-experimental-control.md)
