---
title: Rivian Settings
---

# Rivian Vehicle Settings

Information about sunnypilot behavior on Rivian vehicles. These notes apply when a Rivian vehicle is connected or selected.

**Location**: `Settings -> Vehicle`

---

## Longitudinal Harness Upgrade

Rivian vehicles can gain full longitudinal (speed) control through a custom harness upgrade that includes panda firmware flashing. When this upgrade is installed, sunnypilot gains the following capabilities:

- **Set speed control** via steering wheel buttons: short press for +/- 1 unit, long press (approximately 3 seconds) for +/- 10 km/h or +/- 5 mph
- **Snap to current speed** by holding the stalk for 0.5 seconds
- **Follow distance adjustment** via the right steering wheel scroll
- **Blind spot monitoring** integration from the factory BSM system

!!! note
    This upgrade requires aftermarket hardware modifications. See community resources for installation guidance.

---

## MADS Limitations

Rivian vehicles operate in **limited MADS mode**:

| Setting | Forced Value |
|---------|-------------|
| Toggle with Main Cruise | Off (locked) |
| Unified Engagement Mode | On (locked) |
| Steering Mode on Brake Pedal | Disengage (locked) |

Additionally, lateral control is restricted to a steering angle range of +/- 90 degrees. Beyond this threshold, steering assistance disengages for safety.

See [MADS](../../features/steering/mads.md) for details on limited MADS mode.
