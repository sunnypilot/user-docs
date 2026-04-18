---
title: Subaru Settings
---

# Subaru Vehicle Settings

Settings specific to Subaru vehicles. These appear in the Vehicle panel when a Subaru vehicle is connected or selected.

**Location**: `Settings -> Vehicle`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Stop and Go (Beta)

Enables automatic resume during stop-and-go traffic for supported Subaru platforms. Without this, you must manually resume after a full stop.

!!! note "Availability"
    Can only be changed while the device is offroad. Not available on Global Gen2 or Hybrid platforms.

---

## Stop and Go for Manual Parking Brake (Beta)

Enables stop-and-go for Subaru Global models equipped with a manual handbrake (lever-type parking brake).

!!! warning
    Models with an **electric parking brake** should keep this disabled. This setting is designed specifically for vehicles with a manual/lever parking brake.

!!! note "Availability"
    Can only be changed while the device is offroad. Not available on Global Gen2 or Hybrid platforms.

---

## Pre-Global Vehicle Support

sunnypilot supports Pre-Global Subaru platforms that upstream openpilot treats as dashcam-only. These older model years have simplified CAN architecture and require specialized handling.

Supported Pre-Global vehicles:

| Vehicle | Years |
|---------|-------|
| Subaru Forester | 2017-2018 |
| Subaru Legacy | 2015-2018 |
| Subaru Outback | 2015-2017 |
| Subaru Outback | 2018-2019 |

!!! warning "Steering Only"
    Alpha Longitudinal not available on Pre-Global platforms. Stop-and-go resume works, but no cruise speed adjustment.

!!! note "MADS"
    MADS LKAS button detection not available on Pre-Global vehicles.

!!! warning "Testing Status"
    Pre-Global platforms have active steering enabled on sunnypilot (overriding upstream's dashcam-only default) but have limited community mileage. Validate real-world behavior before relying on them for daily driving.
