---
title: Lane Change Settings
---

# Lane Change Settings

Configure automatic lane change behavior and blind spot monitoring integration.

**Location**: `Settings -> Steering -> Customize Lane Change`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Auto Lane Change by Blinker

A selector that controls how lane changes are initiated when you activate the turn signal. Use the **-** and **+** buttons to cycle through the options:

| Option | What happens |
|--------|-------------|
| **Off** | Auto lane change is disabled |
| **Nudge** | Requires a light steering nudge in the desired direction to start the lane change (default) |
| **Nudgeless** | Lane change begins immediately when the turn signal is activated - no nudge needed |
| **0.5 s** | Lane change begins 0.5 seconds after the turn signal is activated |
| **1 s** | Lane change begins 1 second after activation |
| **2 s** | Lane change begins 2 seconds after activation |
| **3 s** | Lane change begins 3 seconds after activation |

---

## Auto Lane Change: Delay with Blind Spot

When enabled, the system waits for the blind spot to clear before executing a lane change. If a vehicle is detected in the blind spot, the lane change is delayed until the path is clear.

!!! note "Availability"
    This toggle only appears if your vehicle supports Blind Spot Monitoring (BSM) and Auto Lane Change by Blinker is set to a mode other than Off or Nudge.

---

## Related Features

- [Auto Lane Change](../../features/steering/auto-lane-change.md)
