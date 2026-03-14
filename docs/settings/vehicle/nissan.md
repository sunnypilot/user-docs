---
title: Nissan Settings
---

# Nissan Vehicle Settings

Information about sunnypilot behavior on Nissan vehicles. These notes apply when a Nissan vehicle is connected or selected.

**Location**: `Settings -> Vehicle`

---

## ICBM Support

Nissan vehicles support [Intelligent Cruise Button Management (ICBM)](../../features/cruise/icbm.md). Cruise button events (resume/accel and decel/set) are read from the `CRUISE_THROTTLE` CAN message and managed by sunnypilot's ICBM logic to enable features like Speed Limit Assist and Smart Cruise Control on vehicles without native longitudinal control.

---

## Nissan Leaf

The Nissan Leaf uses a dedicated safety configuration within sunnypilot to accommodate its specific CAN bus behavior.
