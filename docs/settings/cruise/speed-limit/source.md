---
title: Speed Limit Source
---

# Speed Limit Source

**Location**: `Settings -> Cruise -> Speed Limit -> Customize Source`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

Configure which data source sunnypilot uses to determine the current speed limit, and how multiple sources are prioritized.

---

## Speed Limit Source

A row of five buttons lets you choose the source policy:

| Option | What it does |
|--------|-------------|
| **Car Only** | Uses only the speed limit data provided by your vehicle's built-in systems (e.g., traffic sign recognition from the car's cameras) |
| **Map Only** | Uses only OpenStreetMap data for speed limits. Requires a downloaded map database from the [OSM panel](../../osm.md) |
| **Car First** | Checks the car's speed limit data first. Falls back to map data if the car does not report a limit |
| **Map First** | Checks map data first. Falls back to the car's reported limit if no map data is available |
| **Combined** | Uses the higher of the two available values from car and map sources |

!!! tip
    **Car First** is a good default for vehicles with traffic sign recognition. If your vehicle does not have sign recognition, use **Map Only** or **Map First** and make sure you have downloaded the map for your region in the [OSM panel](../../osm.md).

---

## Related

- [Speed Limit Settings](index.md) - mode, offset type, and offset value
- [OSM Panel](../../osm.md) - download map data for your region
- [Speed Limit Assist (Feature)](../../../features/cruise/speed-limit.md) - how Speed Limit Assist works
