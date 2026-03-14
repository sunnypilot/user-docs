---
title: Enhanced Smart Cruise Control (ESCC)
---

# Enhanced Smart Cruise Control (ESCC)

## Overview

Enhanced Smart Cruise Control (ESCC) is a sunnypilot feature for Hyundai, Kia, and Genesis **CAN** vehicles (not CAN FD). It integrates data from the Mando radar module directly into sunnypilot's cruise control messages, enabling longitudinal control on vehicles that would otherwise not support it.

## How It Works

On supported vehicles, the Mando radar sends data on CAN message `0x2AB`. When ESCC is enabled, sunnypilot:

1. Receives radar state data including AEB commands and deceleration values
2. Passes these values through to the SCC12 control message that sunnypilot sends to the vehicle
3. Maintains AEB (Automatic Emergency Braking) and FCA (Forward Collision Avoidance) functionality by forwarding the radar's safety signals

### SCC12 Integration

ESCC updates the following fields in the SCC12 message:

| Field | Purpose |
|-------|---------|
| `AEB_CmdAct` | AEB command activation from radar |
| `CF_VSM_Warn` | AEB warning signal |
| `CF_VSM_DecCmdAct` | AEB deceleration command activation |
| `CR_VSM_DecCmd` | AEB deceleration command value |
| `AEB_Status` | Set to enabled (2) to maintain AEB functionality |

## Safety

ESCC preserves all factory safety systems. AEB and FCA alerts from the Mando radar are passed through directly to the vehicle — sunnypilot does not filter or modify these safety-critical signals.

## Requirements

!!! info "Requirements"
    - Hyundai, Kia, or Genesis vehicle using the **CAN** protocol (not CAN FD)
    - Vehicle must have a Mando radar that broadcasts on CAN message `0x2AB`

!!! note "CAN FD"
    ESCC is not applicable to CAN FD vehicles. CAN FD platforms use a different communication protocol and have native SCC support through different mechanisms.

## Related

- [Hyundai / Kia / Genesis Settings](../settings/vehicle/hyundai.md)
- [Alpha Longitudinal](../features/cruise/alpha-longitudinal.md)
- [Hyundai Longitudinal Tuning](hyundai-longitudinal-tuning.md)
