---
title: Alpha Longitudinal
---

# Alpha Longitudinal

## What It Does

Alpha Longitudinal provides experimental longitudinal (speed and acceleration) control for vehicles that are openpilot-compatible but do not have official sunnypilot longitudinal support. This enables throttle and brake control on cars that would otherwise be limited to lateral (steering) assistance only.

For officially supported vehicles, sunnypilot provides refined longitudinal tuning tailored to each platform. Alpha Longitudinal extends this capability to additional vehicles using a more generalized approach, allowing drivers of these cars to experience full ACC-like functionality through sunnypilot.

## How It Works

Alpha Longitudinal uses the vehicle's existing communication interfaces to send throttle and brake commands, bypassing the need for the vehicle's stock cruise control system. The system:

- Reads vehicle speed, pedal position, and other sensor data through the car's CAN bus
- Calculates desired acceleration based on the driving model's output
- Sends throttle and brake commands directly to the vehicle's powertrain controllers
- Sets `pcmCruise=False`, meaning sunnypilot takes full control of longitudinal behavior instead of relying on the vehicle's built-in cruise control module

Because this operates outside the vehicle manufacturer's intended cruise control pathway, the tuning is less refined than on officially supported platforms.

!!! danger "AEB Is Disabled"
    Enabling Alpha Longitudinal **disables your vehicle's Automatic Emergency Braking (AEB)**. This is a significant safety trade-off. Without AEB, the vehicle will not automatically apply emergency braking in imminent collision scenarios. Drive with extra caution and maintain safe following distances at all times.

## Requirements

!!! info "Requirements"
    - Vehicle must be openpilot-compatible (listed on the [comma.ai vehicle compatibility list](https://comma.ai/vehicles))
    - Vehicle does not have official sunnypilot longitudinal support
    - Vehicle must report `CP.alphaLongitudinalAvailable = True` — availability is determined per vehicle in the car interface code
    - Feature is experimental and under active development

!!! warning "Development Branches Only"
    Alpha Longitudinal is flagged as `DEVELOPMENT_ONLY`. It is **only available on development and staging branches**, not on release branches. This is intentional — the feature is not considered stable enough for general release.

!!! warning "Mutually Exclusive with ICBM"
    Alpha Longitudinal and [ICBM](icbm.md) cannot be active at the same time. Enabling Alpha Longitudinal disables ICBM, and vice versa. Alpha Longitudinal provides direct throttle/brake control, while ICBM works through the stock cruise control system — these two approaches are fundamentally incompatible.

!!! warning "Alpha Quality Software"
    This feature is **alpha quality**. Expect rough edges, less smooth acceleration and braking behavior, and less refined stop-and-go performance compared to officially supported vehicles. Longitudinal behavior may vary significantly between vehicle models and driving conditions.

## How to Enable

**Settings** → **Developer** → **sunnypilot Longitudinal Control (Alpha)**

!!! note
    This toggle only appears on development branches and only for vehicles where `alphaLongitudinalAvailable` is `True`.

## Settings Reference

See [Cruise Control Settings](../../settings/cruise/index.md) for configuration details.
