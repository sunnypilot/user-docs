---
title: Hyundai Longitudinal Tuning
---

# Hyundai Longitudinal Tuning Implementation

!!! info "Audience"
    This is advanced technical documentation intended for developers and contributors. End users do not need to understand these details to use sunnypilot.

## Overview

sunnypilot implements custom longitudinal (speed/acceleration) control tuning for Hyundai, Kia, and Genesis (HKG) vehicles. The goal is to produce smooth, comfortable acceleration and deceleration behavior that matches or exceeds the quality of the vehicle's stock adaptive cruise control system.

This tuning layer sits between the driving model's desired acceleration output and the actual commands sent to the vehicle, shaping the acceleration profile to meet comfort and safety constraints.

## Design Goals

The longitudinal tuning for HKG vehicles targets the following objectives:

- **Comfort**: Minimize abrupt speed changes that cause passenger discomfort
- **Smoothness**: Produce acceleration and deceleration curves that feel natural and predictable
- **Safety**: Maintain appropriate following distances and stopping margins
- **Consistency**: Deliver repeatable behavior across different driving conditions
- **Parity with stock**: Match or exceed the refinement of the factory ACC system

## Standards Reference

The tuning implementation references **ISO 15622:2018** (Intelligent Transport Systems — Adaptive Cruise Control Systems — Performance Requirements and Test Procedures). This standard defines:

- Maximum and minimum acceleration/deceleration rates for ACC systems
- Response time requirements for speed changes
- Following distance behavior and time-gap requirements
- Performance criteria for cut-in and cut-out scenarios

## Key Concepts

### Jerk Limiting

**Jerk** is the rate of change of acceleration (m/s³). High jerk values produce the "jerky" feeling passengers experience during abrupt speed changes.

The tuning system limits jerk to keep acceleration transitions smooth:

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Minimum jerk** | 0.5 m/s³ | Floor value — jerk is never reduced below this to maintain responsiveness |
| **Default jerk limit** | 4.0 m/s³ | Standard upper bound for jerk across most driving scenarios |

- Acceleration onset is ramped gradually rather than applied instantly
- Deceleration transitions are similarly smoothed to avoid sudden braking sensations
- Different jerk limits apply to different driving scenarios (e.g., following vs. stopping)

#### Per-Vehicle Jerk Overrides

Some vehicle models have custom jerk limits tuned to their specific powertrain characteristics:

| Vehicle | Jerk Limit (m/s³) | Reason |
|---------|-------------------|--------|
| **Kia Niro EV** | 3.3 | EV powertrain delivers instant torque; lower jerk limit prevents harsh acceleration onset |
| **Kia Niro PHEV (2022+)** | 5.0 | Hybrid powertrain benefits from slightly higher jerk allowance for smoother transitions between electric and ICE modes |

#### Type-Specific Overrides

Jerk limits and acceleration profiles are also adjusted by vehicle communication type:

| Type | Adjustment |
|------|------------|
| **CAN-FD** | Tuning adapted for CAN-FD protocol timing and message rates |
| **EV** | Lower default jerk limits to account for instant torque delivery |
| **Hybrid** | Adjusted profiles to handle transitions between electric and combustion modes |

### Parabolic Approach

When decelerating to a stop or approaching a slower lead vehicle, the system uses **parabolic deceleration profiles** rather than constant-rate braking. This means:

- Deceleration starts gently and increases progressively
- As the vehicle nears the target speed or stop point, deceleration tapers off
- The result is a smooth, gradual stop rather than an abrupt one
- This mimics how experienced human drivers naturally brake

### Speed-Dependent Tuning

Longitudinal behavior is tuned differently across speed ranges:

| Speed Range | Tuning Focus |
|-------------|--------------|
| Low speed (stop-and-go) | Smooth stop/start transitions, creep management |
| City speeds | Responsive acceleration, comfortable following |
| Highway speeds | Gentle speed adjustments, fuel-efficient cruising |

Parameters such as acceleration limits, jerk bounds, and following distance gains are adjusted based on the current vehicle speed to optimize behavior for each regime.

### Lead Vehicle Response

The system adapts its behavior based on the lead vehicle's actions:

- **Lead accelerating**: Gradual acceleration to maintain gap without aggressive throttle
- **Lead decelerating**: Proportional braking response with jerk limiting
- **Lead cut-in**: Timely but smooth deceleration to establish safe following distance
- **Lead cut-out**: Controlled acceleration to resume set speed

## Panda Safety Limits

The panda enforces hard acceleration limits at the firmware level that cannot be overridden:

| Parameter | Limit |
|-----------|-------|
| **Maximum acceleration** | +2.0 m/s² |
| **Maximum deceleration** | -3.5 m/s² |

All tuning parameters must produce acceleration commands within these bounds. Any command exceeding these limits is clamped by the panda safety layer.

## Technical Parameters

The tuning system uses several categories of parameters:

- **Acceleration bounds**: Maximum and minimum acceleration values at different speeds
- **Jerk limits**: Rate-of-change constraints for both positive and negative acceleration (min: 0.5, default max: 4.0 m/s³)
- **Time constants**: Filtering and smoothing time constants for acceleration commands
- **Following distance gains**: Speed-dependent proportional and derivative gains for gap control
- **Stopping parameters**: Deceleration profiles and creep behavior for stop-and-go

!!! tip "Contributing"
    If you are working on longitudinal tuning for HKG vehicles, test changes thoroughly across multiple driving scenarios — highway cruising, city stop-and-go, and lead vehicle cut-in/cut-out — before submitting a pull request.

## Related Pages

- [Cruise Control Settings](../settings/cruise/index.md) — User-facing cruise control configuration
- [Hyundai Vehicle Settings](../settings/vehicle/hyundai.md) — Hyundai-specific settings reference
