---
title: Smart Cruise Control - Vision
---

# Smart Cruise Control — Vision (SCC-V)

## What It Does

SCC-V uses the device's camera to monitor the road ahead and predict upcoming turns. It calculates lateral acceleration from the model's predicted path and smoothly reduces cruise speed before curves, then restores it after exiting. This applies regardless of whether sunnypilot or the vehicle's stock system is handling longitudinal control.

## How It Works

The neural network continuously outputs a predicted path and velocity profile. SCC-V samples the predicted lateral acceleration at the 97th percentile across a forward time window. When that value exceeds a threshold, SCC-V transitions through its state machine and outputs a lower target speed. Once the curve clears, it ramps the target speed back up.

SCC-V operates on top of whichever longitudinal control method is active:

- **With sunnypilot longitudinal control** (native or [Alpha](alpha-longitudinal.md)): the target speed is fed directly into the longitudinal planner, which uses it to command throttle and brake
- **With [ICBM](icbm.md)**: the target speed is fed through the same planner, and ICBM simulates cruise button presses to reach it via the stock cruise control system

The minimum operating speed is 12 mph (20 km/h). Below that threshold, SCC-V is inactive.

## Requirements

!!! info "Requirements"
    - Either sunnypilot longitudinal control (native or [Alpha](alpha-longitudinal.md)) **or** [ICBM](icbm.md) must be active
    - Camera must have a clear view of the road ahead

## How to Enable

**Settings** → **Cruise** → **Smart Cruise Control — Vision**

The toggle is always visible but disabled unless at least one of the above longitudinal control methods is active.

## Settings Reference

See [Cruise Control Settings](../../settings/cruise/index.md) for configuration details.
