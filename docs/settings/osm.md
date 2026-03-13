---
title: OSM Settings
---

# OSM Settings

Download and manage OpenStreetMap (OSM) data used for speed limit lookups, curve detection, and road name display.

**Location**: `Settings -> OSM`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Mapd Version

Displays the version of the map processing daemon currently running on the device.

---

## Downloaded Maps

Shows the current size of downloaded map data. A **DELETE** button removes all downloaded map files to free storage space.

!!! note "Availability"
    The delete button is disabled while a map download is in progress.

---

## Downloading Map

A progress indicator that appears only while a map download or database check is active. Shows the download percentage and the file being downloaded.

---

## Database Update

A **CHECK** button that checks for updates to your selected region's OSM database. After checking, it downloads any available updates. The description shows the last check time or current download progress.

!!! note "Availability"
    Only appears when a country has been selected. Disabled while a download is in progress.

---

## Country

A **SELECT** button that opens a country selection dialog. Choose the country for which you want to download map data. The currently selected country is displayed.

!!! note "Availability"
    Disabled while a download is in progress.

---

## State

A **SELECT** button that opens a US state selection dialog. Narrows the download to a specific state, reducing download size and improving performance.

!!! note "Availability"
    Only appears when the selected country is the United States. Disabled while a download is in progress.

---

## Related Features

- [OSM Maps](../features/connected/osm-maps.md)
- [Speed Limit Assist](../features/cruise/speed-limit.md)
- [Smart Cruise Control - Map](../features/cruise/scc-m.md)
