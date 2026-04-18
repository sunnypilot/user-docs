---
title: Hyundai / Kia / Genesis Settings
---

# Hyundai / Kia / Genesis Vehicle Settings

Settings specific to Hyundai, Kia, and Genesis vehicles. These appear in the Vehicle panel when a supported vehicle is connected or selected.

**Location**: `Settings -> Vehicle`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Custom Longitudinal Tuning

A row of three buttons that selects a longitudinal (speed) control tuning profile:

| Option | Behavior |
|--------|----------|
| **Off** | Default tuning with standard acceleration and braking |
| **Dynamic** | More responsive acceleration and braking for a sportier feel |
| **Predictive** | Smoother, anticipatory speed changes that prioritize comfort |

!!! note "Availability"
    Requires sunnypilot Longitudinal Control (Alpha) to be enabled. Can only be changed while the device is offroad. Hidden on vehicles that do not support alpha longitudinal control.

---

## Enhanced Smart Cruise Control (ESCC)

On CAN-based Hyundai, Kia, and Genesis vehicles (not CAN FD), sunnypilot can integrate data from the Mando radar to enable longitudinal control. ESCC passes through AEB and FCA safety signals from the radar, preserving all factory safety systems.

ESCC is automatically detected during vehicle fingerprinting when the Mando radar broadcast is present on the CAN bus. No user configuration is needed.

See [Enhanced Smart Cruise Control (ESCC)](../../technical/escc.md) for technical details.

!!! note "CAN Only"
    ESCC applies only to vehicles using the CAN protocol. CAN FD vehicles use different mechanisms for SCC support.

---

## Speed Limit Sources

Hyundai, Kia, and Genesis vehicles can provide speed limit data from two on-board sources:

| Source | Signal | Priority |
|--------|--------|----------|
| **Camera** | LKAS12 `CF_Lkas_TsrSpeed_Display_Clu` | Primary |
| **Navigation** | `Navi_HU.SpeedLim_Nav_Clu` | Secondary |

Camera-detected speed limits take priority over navigation-based limits. CAN FD vehicles use the `FR_CMR_02` message instead.

Source availability depends on which CAN messages your vehicle broadcasts — this is automatically detected during fingerprinting. Not all vehicles have both sources.

These on-board sources supplement OSM-based speed limits. See [Speed Limit Assist](../../features/cruise/speed-limit.md) for details.

---

## MADS Support

Hyundai, Kia, and Genesis vehicles support [MADS](../../features/steering/mads.md) (Modular Assistive Driving System) via the **LDA button** (the physical button that toggles stock Lane Following Assist). The system manages LFA icon states on the dashboard to indicate lateral control status.

On vehicles with the LDA button or CAN FD, MADS can be used even without active cruise state available.

!!! note
    Only the LDA button is supported for MADS toggling. The LKAS button is not currently supported on Hyundai/Kia/Genesis vehicles.

---

## Intelligent Cruise Button Management (ICBM)

Hyundai, Kia, and Genesis vehicles support [ICBM](../../features/cruise/icbm.md) for automatic cruise speed management. Both CAN and CAN FD vehicles are supported.

<details><summary>Technical details</summary>

- **CAN vehicles:** ICBM sends cruise button commands via the CLU11 message
- **CAN FD vehicles:** ICBM uses button counter cycling

</details>

ICBM appears in [Cruise Settings](../cruise/index.md) when a supported vehicle is connected.

---

## Non-SCC Vehicle Support

sunnypilot supports certain Hyundai, Kia, and Genesis vehicles that lack factory Smart Cruise Control (SCC). This includes ICE, Hybrid, and EV variants. On these vehicles, sunnypilot uses alternative CAN message parsing to provide steering assistance. No longitudinal control is available — steering-only.

Supported Non-SCC vehicles:

- Hyundai Elantra 2022
- Hyundai Kona 2019
- Hyundai Kona EV 2019
- Kia Ceed PHEV 2022
- Kia Forte 2019

!!! warning "Testing Status"
    Some Non-SCC platforms are in dashcam mode (untested). These vehicles run sunnypilot in a monitoring-only mode until community testing validates full steering support.
