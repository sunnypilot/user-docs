---
title: Tesla Settings
---

# Tesla Vehicle Settings

Settings specific to Tesla vehicles. These appear in the Vehicle panel when a Tesla vehicle is connected or selected.

**Location**: `Settings -> Vehicle`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Cooperative Steering (Beta)

Allows the driver to provide limited steering input while sunnypilot is engaged, rather than requiring a full override or disengage to steer manually. Only works above 23 km/h (14 mph).

!!! warning
    May cause steering oscillations below 48 km/h (30 mph) during turns. Disable this feature if you experience oscillations.

!!! note "Availability"
    Can only be changed while the device is offroad. Use "Always Offroad" in [Device Settings](../device.md) to change this while the vehicle is running.

---

## MADS Limitations

Tesla vehicles **without a vehicle bus connection** operate in limited MADS mode:

| Setting | Forced Value |
|---------|-------------|
| Toggle with Main Cruise | Off (locked) |
| Unified Engagement Mode | On (locked) |
| Steering Mode on Brake Pedal | Disengage (locked) |

See [MADS Settings](../steering/mads.md) for details.

---

## Speed Limit Assist Restrictions

On **release branches**, Speed Limit Assist mode is disabled for Tesla vehicles. Info and Warning modes remain available.

See [Speed Limit Settings](../cruise/speed-limit/index.md) for details.
