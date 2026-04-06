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
| **Combined** | Uses the lowest (most conservative) value from either source |

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

## Behavior by Vehicle Configuration

Assist mode behavior varies depending on how your vehicle handles longitudinal control. Information and Warning modes work the same across all configurations.

### PCM Cruise vehicles

Applies to vehicles where sunnypilot controls acceleration and braking but the stock cruise module (PCM) remains active and controls the instrument cluster set speed display. sunnypilot cannot directly override the cluster set speed on these vehicles.

This includes: Toyota / Lexus, Honda (Nidec), Ford, Tesla, Rivian, and Subaru — when sunnypilot longitudinal control is enabled.

- The cruise set speed shown on the instrument cluster displays a **fixed high value** (not the actual speed limit) — this signals that SLA is managing the target speed
- The actual speed limiting happens at the software level
- Manually changing the cruise set speed deactivates SLA, and you must disengage and re-engage to use SLA again

**When the speed limit changes while SLA is active:**

- If the current and new speed limits are **both at or above 50 mph (80 km/h):** the new limit is adopted automatically
- Otherwise, SLA enters a **pre-active** state for up to **15 seconds**
- Confirmation happens automatically when the cluster speed matches the expected target — no button press is needed
- If not confirmed within 15 seconds, SLA returns to inactive

<details><summary>Why does the cluster show a high speed?</summary>

Because the stock cruise module controls the instrument cluster display, sunnypilot cannot show the actual speed limit on the cluster. Instead, it sets the cluster to a high ceiling value (120-130 km/h or 70-80 mph depending on the speed limit) to indicate that SLA is active. The actual speed control uses the detected speed limit internally.

The two-tier ceiling prevents unnecessarily high displayed values for lower speed limits:

- Speed limit below 80 km/h (50 mph): cluster shows 120 km/h (70 mph)
- Speed limit at or above 80 km/h (50 mph): cluster shows 130 km/h (80 mph)

</details>

### Non-PCM Cruise vehicles

Applies to vehicles where sunnypilot fully controls acceleration and braking **and** the stock cruise module is not active. sunnypilot directly manages the cruise set speed.

This includes: Hyundai / Kia / Genesis, Honda (Bosch), GM, and Volkswagen — when sunnypilot longitudinal control is enabled.

- The cruise set speed on the display shows the **actual speed limit** (with offset)
- Manually changing the cruise set speed while SLA is active deactivates it

**When the speed limit changes while SLA is active:**

- If your cruise set speed and the new speed limit are **both at or above 50 mph (80 km/h):** the set speed adjusts automatically
- Otherwise, SLA enters a **pre-active** state for up to **5 seconds** and waits for confirmation
- **To confirm:** press the cruise button in the correct direction (+ if the new limit is higher, - if lower), or let the set speed match automatically
- If not confirmed within 5 seconds, SLA returns to inactive

### ICBM vehicles

Applies to vehicles using [ICBM](icbm.md) for cruise speed management instead of sunnypilot longitudinal control. ICBM physically presses cruise buttons to match the target speed.

This includes: Chrysler / Dodge / Jeep / RAM, Mazda, Honda, and Hyundai / Kia / Genesis — when ICBM is enabled.

- SLA computes the target speed, and ICBM adjusts the stock cruise to match
- The cruise set speed on the display shows the **actual speed limit** (with offset)
- Manually changing the cruise set speed while SLA is active deactivates it

**When the speed limit changes while SLA is active:**

- If your cruise set speed and the new speed limit are **both at or above 50 mph (80 km/h):** the set speed adjusts automatically
- Otherwise, SLA enters a **pre-active** state for up to **5 seconds** and waits for confirmation
- **To confirm:** press the cruise button in the correct direction (+ or -)
- If not confirmed within 5 seconds, SLA returns to inactive

!!! note
    The confirmation button press is intercepted by SLA and does not also adjust the set speed — it only confirms the speed limit change.

### Stock cruise without ICBM

If your vehicle uses stock cruise control and ICBM is not enabled, **Assist mode is not available**. SLA has no mechanism to adjust the cruise set speed. Information and Warning modes still work normally.

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
    - **Stock cruise without ICBM:** Assist mode is not available (no mechanism to adjust set speed)

## Settings Reference

See [Speed Limit Settings](../../settings/cruise/speed-limit/index.md) for all configuration options.
