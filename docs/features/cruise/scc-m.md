---
title: Smart Cruise Control - Map
---

# Smart Cruise Control — Map (SCC-M)

## What It Does

SCC-M uses downloaded OpenStreetMap data to anticipate upcoming curves, speed limit zones, and intersections. It calculates the deceleration needed to reach a safe target speed before each waypoint and outputs a smoothed velocity profile using jerk-based planning. This applies regardless of whether sunnypilot or the vehicle's stock system is handling longitudinal control.

## How It Works

1. OSM map data is loaded and matched to the vehicle's current GPS position
2. Upcoming waypoints with target velocities are identified (curves, speed zones, intersections)
3. SCC-M calculates the required deceleration to arrive at each waypoint at the correct speed
4. A smoothed target speed is output and fed into the longitudinal planner

SCC-M operates on top of whichever longitudinal control method is active:

- **With sunnypilot longitudinal control** (native or [Alpha](alpha-longitudinal.md)): the target speed is fed directly into the longitudinal planner, which uses it to command throttle and brake
- **With [ICBM](icbm.md)**: the target speed is fed through the same planner, and ICBM simulates cruise button presses to reach it via the stock cruise control system

The minimum operating speed is 12 mph (20 km/h). Below that threshold, SCC-M is inactive.

## Requirements

!!! info "Requirements"
    - Either sunnypilot longitudinal control (native or [Alpha](alpha-longitudinal.md)) **or** [ICBM](icbm.md) must be active
    - [OSM Maps](../connected/osm-maps.md) must be configured and map data downloaded for your region

## How to Enable

**Settings** → **Cruise** → **Smart Cruise Control — Map**

The toggle is always visible but disabled unless at least one of the above longitudinal control methods is active.

## Settings Reference

See [Cruise Control Settings](../../settings/cruise/index.md) for configuration details.
