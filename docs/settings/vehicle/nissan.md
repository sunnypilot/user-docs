---
title: Nissan Settings
---

# Nissan Vehicle Settings

Information about sunnypilot behavior on Nissan vehicles. These notes apply when a Nissan vehicle is connected or selected.

**Location**: `Settings -> Vehicle`

---

## Nissan Leaf

The Nissan Leaf uses a dedicated safety configuration within sunnypilot to accommodate its specific CAN bus behavior. Key differences include:

- **Brake and accelerator signals**: The Leaf uses different CAN message sources for brake and accelerator detection compared to other Nissan models
- **Seatbelt-based cancel**: Cruise control cancellation is triggered by seatbelt unbuckling rather than the standard cancel button path
- **Dedicated safety model**: A separate safety configuration ensures correct signal boundaries for the Leaf's unique powertrain interface

---

## Cruise Button Events

Nissan vehicles forward cruise button events (resume/accel and decel/set) from the `CRUISE_THROTTLE` CAN message to sunnypilot. This is basic button event handling used for standard cruise control interaction — it is not the [Intelligent Cruise Button Management (ICBM)](../../features/cruise/icbm.md) speed management system. ICBM is not available on Nissan vehicles.
