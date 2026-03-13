---
title: Smart Cruise Control - Map
---

# Smart Cruise Control — Map (SCC-M)

## What It Does

SCC-M uses downloaded OpenStreetMap data to anticipate road changes — curves, speed limits, and intersections — and adjusts cruise speed proactively through [ICBM](icbm.md).

## How It Works

1. OSM map data provides information about upcoming road geometry
2. SCC-M calculates appropriate speeds for curves, speed zones, and intersections
3. Speed commands are sent through ICBM to adjust cruise before reaching these road features

## Requirements

!!! info "Requirements"
    - [ICBM](icbm.md) must be enabled
    - Vehicle must support ICBM
    - [OSM Maps](../connected/osm-maps.md) must be configured and downloaded

## How to Enable

**Settings** → **Cruise** → **Smart Cruise Control — Map**

## Settings Reference

See [Cruise Control Settings](../../settings/cruise/index.md) for configuration details.
