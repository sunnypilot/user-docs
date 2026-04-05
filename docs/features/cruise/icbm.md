---
title: Intelligent Cruise Button Management
---

# Intelligent Cruise Button Management (ICBM)

## What It Does

ICBM allows sunnypilot to intercept and dynamically manage your vehicle's cruise control button presses. Instead of directly changing the set speed, button presses are routed through sunnypilot's logic, enabling features like Speed Limit Assist and Smart Cruise Control on vehicles that don't natively support sunnypilot longitudinal control.

This is particularly useful for vehicles where sunnypilot cannot directly control acceleration and braking — ICBM gives you many of the same benefits by intelligently managing the cruise buttons.

## When to Use

ICBM is designed specifically for vehicles where sunnypilot cannot directly control acceleration and braking (i.e., no native longitudinal control). On these vehicles, the stock cruise control system still handles all speed control. ICBM bridges the gap by intelligently managing cruise button commands so you can still benefit from sunnypilot's speed planning features.

## How It Works

1. You press the cruise speed button on your steering wheel
2. ICBM intercepts the button press
3. sunnypilot applies its logic (speed limits, map curves, etc.) to determine the appropriate speed change
4. ICBM simulates the corresponding cruise button presses over the CAN bus, sending the adjusted command to the vehicle's stock cruise control system

This happens transparently — from your perspective, the buttons work normally but with smarter behavior. Under the hood, ICBM is communicating with the vehicle's cruise control module by simulating physical button presses on the CAN bus, which is why it works even on vehicles without direct throttle/brake control.

### State Machine

ICBM operates through a 5-state machine:

| State | Description |
|-------|-------------|
| **Inactive** | ICBM is idle — no button simulation is in progress |
| **Pre-Active** | A speed change has been requested; ICBM is preparing to simulate button presses |
| **Increasing** | ICBM is sending "speed up" button presses to reach the target speed |
| **Decreasing** | ICBM is sending "speed down" button presses to reach the target speed |
| **Holding** | Target speed has been reached; ICBM is holding the current setting |

!!! tip "Safety"
    ICBM preserves all of your vehicle's stock safety systems. Forward Collision Avoidance (FCA), Automatic Emergency Braking (AEB), and other factory safety features remain fully active and unaffected, since the vehicle's own cruise control system is still performing the actual speed control. ICBM operates purely at the CAN bus button simulation level and does not interact with FCA or AEB message pathways.

## Supported Vehicles

ICBM support varies by vehicle brand. The feature toggle only appears in settings if your vehicle is supported.

| Brand | Notes |
|-------|-------|
| **Hyundai / Kia / Genesis** | Most CAN models. Not available on vehicles with CAN FD alternate buttons. |
| **Honda / Acura** | Bosch non-CAN FD platforms. CAN FD Honda models may have ICBM on development branches only. |
| **Chrysler / Dodge / Jeep / RAM** | All platforms |
| **Mazda** | All platforms |

!!! info "Not Listed?"
    If your brand or model is not listed above and the ICBM toggle does not appear in your settings, your vehicle is not currently supported. Support depends on the vehicle's CAN bus protocol and button command structure.

## Requirements

!!! info "Requirements"
    - Your vehicle must support ICBM — not all vehicles are compatible
    - If the ICBM toggle does not appear in settings, your vehicle is not supported
    - **Mutually exclusive with [Alpha Longitudinal](alpha-longitudinal.md)** — only one can be active at a time

## How to Enable

**Settings** → **Cruise** → **Intelligent Cruise Button Management**

## Features Enabled by ICBM

When ICBM is enabled, the following features become available on vehicles without native longitudinal control:

- **[Smart Cruise Control — Vision](scc-v.md)** — Vision-based speed adjustments for upcoming curves
- **[Smart Cruise Control — Map](scc-m.md)** — Map-aware speed adjustments for curves, speed zones, and intersections
- **[Custom ACC Increments](custom-acc-increments.md)** — Custom button press speed steps
- **[Speed Limit Assist](speed-limit.md)** — Automatic speed limit matching

!!! note "SCC-V and SCC-M are not exclusive to ICBM"
    Smart Cruise Control — Vision and Smart Cruise Control — Map also work when sunnypilot longitudinal control is active (native or [Alpha](alpha-longitudinal.md)). In that case, their speed targets are fed directly into the longitudinal planner rather than through cruise button simulation.

## Settings Reference

See [Cruise Control Settings](../../settings/cruise/index.md) for all available options.
