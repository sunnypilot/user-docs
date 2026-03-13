---
title: MADS Settings
---

# MADS Settings

Fine-tune how the Modular Assistive Driving System (MADS) engages and disengages steering assistance.

**Location**: `Settings -> Steering -> Customize MADS`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

!!! info "Prerequisite"
    The main **Modular Assistive Driving System (MADS)** toggle must be enabled in [Steering Settings](index.md) to access this sub-panel.

---

## Toggle with Main Cruise

When enabled, pressing the main cruise button (the on/off button on the steering wheel) can activate MADS steering assistance.

!!! warning "Vehicle Restrictions"
    - **Rivian**: Always forced OFF (limited settings mode)
    - **Tesla (without vehicle bus)**: Always forced OFF (limited settings mode)

!!! note
    For vehicles without a dedicated LFA/LKAS button, disabling this will prevent lateral control engagement.

---

## Unified Engagement Mode (UEM)

When enabled, engaging cruise control also automatically engages MADS lateral control in a single action, rather than requiring separate activation.

Once lateral control is engaged via UEM, it remains engaged until you manually disable it using the MADS button or turn off the car.

!!! warning "Vehicle Restrictions"
    - **Rivian**: Always forced ON (limited settings mode)
    - **Tesla (without vehicle bus)**: Always forced ON (limited settings mode)

---

## Steering Mode on Brake Pedal

A row of three buttons controls what happens to MADS steering assistance when you press the brake pedal:

| Mode | What happens |
|------|-------------|
| **Remain Active** | Steering assistance continues even after you press the brake |
| **Pause** | Steering assistance pauses but can be quickly resumed |
| **Disengage** | Steering assistance fully disengages when you brake |

!!! warning "Vehicle Restrictions"
    - **Rivian**: Always forced to Disengage (limited settings mode)
    - **Tesla (without vehicle bus)**: Always forced to Disengage (limited settings mode)

---

## Related Features

- [Modular Assistive Driving System](../../features/steering/mads.md)
