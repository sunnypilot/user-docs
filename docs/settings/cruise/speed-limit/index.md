---
title: Speed Limit Settings
---

# Speed Limit Settings

Configure how sunnypilot responds to detected speed limits from maps, signs, and navigation data.

**Location**: `Settings -> Cruise -> Speed Limit`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Speed Limit

A row of four buttons that controls how sunnypilot uses speed limit information:

| Mode | What it does |
|------|-------------|
| **Off** | Speed limit data is not used |
| **Info** | Displays the current speed limit on the HUD |
| **Warning** | Displays speed limit and alerts you when exceeding it |
| **Assist** | Automatically adjusts cruise speed to match the speed limit (with optional offset) |

!!! note "Availability"
    Requires longitudinal control, or ICBM must be enabled.

!!! warning "Vehicle Restrictions"
    - **Tesla**: Speed Limit Assist mode is disabled on release branches
    - **Rivian**: Speed Limit Assist mode is always disabled

---

## Customize Source

A button that opens the [Speed Limit Source sub-panel](source.md) where you choose which data source provides speed limit information (car, map, or a combination).

---

## Speed Limit Offset

A row of three buttons that controls how the speed offset is calculated:

| Type | What it does |
|------|-------------|
| **None** | No offset - cruise matches the exact speed limit |
| **Fixed** | A fixed value (in km/h or mph) is added to or subtracted from the limit |
| **%** | A percentage is applied to the speed limit |

---

## Speed Limit Value Offset

A slider that sets the offset value applied to the detected speed limit. Use the **-** and **+** buttons to adjust from -30 to +30. This slider only appears when Speed Limit Offset is set to Fixed or %.

- **Positive values**: Cruise faster than the limit (e.g., +5 means 5 over)
- **Negative values**: Cruise slower than the limit (e.g., -5 means 5 under)

---

## Related Features

- [Speed Limit Assist](../../../features/cruise/speed-limit.md)
- [OSM Maps](../../../features/connected/osm-maps.md)
