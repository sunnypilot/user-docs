---
title: Speed Limit Assist
---

# Speed Limit Assist

## What It Does

Speed Limit Assist detects the current speed limit and can automatically adjust your cruise speed to match. It offers four operating modes ranging from passive information display to active speed management.

## How It Works

1. sunnypilot reads speed limit data from two sources (see below)
2. A configurable **Speed Limit Policy** determines how the sources are combined when both are available
3. Based on your chosen mode, the system displays, warns, or actively adjusts your set speed
4. An optional offset (fixed or percentage) lets you cruise slightly above or below the limit

## Speed Limit Sources

Speed Limit Assist pulls speed limit data from **two sources**:

| Source | Description |
|--------|-------------|
| **Car State** | Speed limit information provided by the vehicle's built-in sensors (e.g., Traffic Sign Recognition cameras). Availability depends on the vehicle. |
| **Map Data** | Speed limits from downloaded OpenStreetMap data. Requires [OSM Maps](../connected/osm-maps.md) to be configured and downloaded. |

### Speed Limit Policy

When both sources are available and report different values, the **Speed Limit Policy** setting determines which source is used:

| Policy | Behavior |
|--------|----------|
| **Car State Only** | Uses only the vehicle's built-in speed limit data; ignores map data |
| **Map Data Only** | Uses only OSM map speed limit data; ignores car state |
| **Car State Priority** | Uses car state data when available; falls back to map data |
| **Map Data Priority** | Uses map data when available; falls back to car state |
| **Combined** | Uses the highest-confidence value from either source |

## Operating Modes

| Mode | Behavior |
|------|----------|
| **Off** | Speed limit data is not used |
| **Information** | Shows the current speed limit on the driving display |
| **Warning** | Shows the speed limit and alerts you when you're exceeding it |
| **Assist** | Automatically adjusts cruise speed to match the speed limit |

## Speed Offset

You can set an offset so your cruise speed differs from the exact limit:

- **Fixed offset:** Add or subtract a set number of km/h or mph (range: -30 to +30)
- **Percentage offset:** Apply a percentage above or below the limit

## Confirmation Modes

When the detected speed limit changes, you can choose how the system responds:

| Mode | Behavior |
|------|----------|
| **Auto** | The cruise set speed adjusts automatically when a new speed limit is detected — no driver input required |
| **User Confirm** | The system displays the new speed limit and waits for the driver to confirm before adjusting the set speed |

## Driver Notifications

Speed Limit Assist provides visual indicators on the driving HUD:

- The currently detected speed limit is shown on the display
- When a speed limit change is detected, a notification appears showing the new limit
- In Warning and Assist modes, alerts notify you when you are exceeding the posted limit

## Requirements

!!! info "Requirements"
    - Longitudinal control must be available, **or** [ICBM](icbm.md) must be enabled
    - For map-based limits: [OSM Maps](../connected/osm-maps.md) must be configured and downloaded

## How to Enable

**Settings** → **Cruise** → **Speed Limit Assist**

## Vehicle Restrictions

!!! warning "Vehicle Restrictions"
    - **Tesla:** Assist mode is disabled on release branches (Information and Warning still work)
    - **Rivian:** Assist mode is always disabled

## Settings Reference

See [Speed Limit Settings](../../settings/cruise/speed-limit/index.md) for all configuration options.
