---
title: Auto Lane Change
---

# Auto Lane Change

## What It Does

Automatically executes lane changes when you activate the turn signal. You can choose between nudge-based confirmation, nudgeless (immediate), or timed delays before the lane change begins.

## How It Works

1. Activate your turn signal in the desired direction
2. The system verifies that clear lane markings are detected by the vision system in the target lane — a lane change will not execute without visible lane lines
3. The driver monitoring system checks that the driver is attentive before proceeding
4. Depending on your setting:
    - **Nudge:** Give a light steering nudge to confirm the lane change
    - **Nudgeless:** The lane change begins immediately
    - **Timed (0.5s–3s):** The lane change begins after the configured delay
5. If BSM Delay is enabled and a vehicle is detected in your blind spot, the lane change is delayed by an additional 1 second beyond the configured timer

## Requirements

!!! info "Requirements"
    - Lateral control must be active (sunnypilot must be engaged)
    - Vehicle must be traveling above a minimum speed threshold
    - Clear lane markings must be visible to the vision system
    - Driver must be attentive (monitored by the driver monitoring system)

## How to Enable

**Settings** → **Steering** → **Customize Lane Change**

## Modes

| Mode | Value | Behavior |
|------|-------|----------|
| **Off** | -1 | Auto lane change is disabled |
| **Nudge** | 0 | Requires a light steering nudge to confirm the lane change |
| **Nudgeless** | 1 | Lane change begins as soon as you signal |
| **0.5 second** | 2 | Lane change begins after 0.5s delay |
| **1 second** | 3 | Lane change begins after 1s delay |
| **2 seconds** | 4 | Lane change begins after 2s delay |
| **3 seconds** | 5 | Lane change begins after 3s delay |

## Blind Spot Monitoring Integration

If your vehicle supports BSM and the BSM Delay option is enabled, the system checks for vehicles in your blind spot before executing the lane change. When a vehicle is detected in the blind spot, the lane change is delayed by an additional **1 second** on top of the configured timer until the adjacent lane is clear.

!!! info "BSM Requirements"
    - Vehicle must support Blind Spot Monitoring
    - Auto Lane Change Timer must be set beyond Nudge mode

## Settings Reference

See [Lane Change Settings](../../settings/steering/lane-change.md) for all options.

!!! warning "Safety"
    Always check your mirrors and blind spots before initiating a lane change. The system assists but does not replace driver awareness.
