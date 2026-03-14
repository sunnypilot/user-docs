---
title: Enhanced Smart Cruise Control (ESCC)
---

# Enhanced Smart Cruise Control (ESCC)

## Overview

Enhanced Smart Cruise Control (ESCC) is a hardware module for Hyundai, Kia, and Genesis **CAN** vehicles (not CAN FD), similar in concept to Toyota's [SDSU](sdsu.md). It is installed at the SCC radar and enables longitudinal control while retaining factory FCW (Forward Collision Warning) and AEB (Automatic Emergency Braking) functionality.

ESCC provides single-lead tracking. It does not natively enable full radar tracks.

## Why ESCC Exists

Some HKG CAN vehicles can only enable sunnypilot longitudinal control by disabling the radar in software. While this works, it disables factory FCW and AEB — critical safety systems. ESCC solves this by intercepting the SCC messages at the radar so that sunnypilot's commands do not collide with the radar's own messages. This allows longitudinal control without sacrificing factory safety.

Cars with camera-based SCC (where SCC messages originate from the camera rather than the radar) do not need ESCC, because sunnypilot can intercept that traffic directly.

## How It Works

The ESCC module sits at the SCC radar and intercepts messages that sunnypilot needs to send to the vehicle, preventing collisions between the radar's messages and sunnypilot's commands. Its firmware emits data on CAN message `0x2AB`. sunnypilot:

1. Receives radar state data including AEB commands and deceleration values
2. Passes these values through to the SCC12 control message that sunnypilot sends to the vehicle
3. Maintains AEB and FCA (Forward Collision Avoidance) functionality by forwarding the safety signals

### SCC12 Integration

ESCC updates the following fields in the SCC12 message:

| Field | Purpose |
|-------|---------|
| `AEB_CmdAct` | AEB command activation |
| `CF_VSM_Warn` | AEB warning signal |
| `CF_VSM_DecCmdAct` | AEB deceleration command activation |
| `CR_VSM_DecCmd` | AEB deceleration command value |
| `AEB_Status` | Set to enabled (2) to maintain AEB functionality |

## Safety

ESCC preserves all factory safety systems. AEB and FCA alerts are passed through directly to the vehicle — sunnypilot does not filter or modify these safety-critical signals.

## Requirements

!!! info "Requirements"
    - Hyundai, Kia, or Genesis vehicle using the **CAN** protocol (not CAN FD)
    - An ESCC module installed at the SCC radar

!!! tip "Detection"
    sunnypilot automatically detects the ESCC module during vehicle fingerprinting as long as the firmware emits CAN message `0x2AB`. No additional user configuration is needed.

!!! note "CAN FD"
    ESCC is not applicable to CAN FD vehicles. CAN FD platforms use a different communication protocol and have native SCC support through different mechanisms.

## Related

- [SDSU](sdsu.md) — Equivalent hardware module for Toyota/Lexus
- [Hyundai / Kia / Genesis Settings](../settings/vehicle/hyundai.md)
- [Alpha Longitudinal](../features/cruise/alpha-longitudinal.md)
- [Hyundai Longitudinal Tuning](hyundai-longitudinal-tuning.md)
