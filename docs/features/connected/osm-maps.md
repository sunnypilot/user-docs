---
title: OSM Maps
---

# OSM Maps

## What It Does

Integrates OpenStreetMap (OSM) data to provide speed limit information, road geometry, and other map attributes. This data powers features like Speed Limit Assist and Smart Cruise Control — Map.

## How It Works

1. Select your country (and state, if in the US)
2. Download the map data to your device
3. The map daemon processes the data and makes it available to driving features
4. Periodically check for updates to keep your map data current

## Requirements

!!! info "Requirements"
    - Internet connection for initial download and updates
    - Storage space on the device for map data

## How to Set Up

**Settings** → **OSM**

1. Select your **Country**
2. If in the US, select your **State**
3. Tap **Database Update** to download
4. Wait for the download to complete

## Features That Use OSM Data

- **[Speed Limit Assist](../cruise/speed-limit.md)** — Reads speed limits from map data
- **[Smart Cruise Control — Map](../cruise/scc-m.md)** — Uses road geometry for proactive speed adjustment

## Managing Map Data

- **Update:** Tap "Database Update" to check for newer map data
- **Delete:** Tap "Delete Maps" to remove downloaded data and free storage

## Settings Reference

See [OSM Settings](../../settings/osm.md) for all options and status information.
