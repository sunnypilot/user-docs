---
title: Platform Differences
---

# Platform Differences

sunnypilot runs on different hardware platforms, each with its own settings interface. This page explains the differences so you know what to expect.

## Platforms

### comma 3X / comma 3 (TIZI/TICI)

The full-featured interface with a sidebar-based settings panel. All settings and onroad visual features documented in this manual are available on these devices.

### comma four (MICI)

A simplified, touch-friendly interface designed for the comma four's compact form factor. Only a subset of settings are exposed through the on-device screen. Most features still work on comma four - you configure the hidden ones through sunnylink.

However, some onroad visual features require UI rendering code that does not exist on comma four. These features cannot be activated on comma four even through sunnylink. Each setting page notes which category it falls into.

### sunnylink (Web / App)

The sunnylink web interface provides access to all configurable settings regardless of which device you use. If a setting is not shown on your comma four's screen, you can configure it through sunnylink - provided the feature is supported on your device.

## Three Levels of Device Availability

Throughout this manual, each setting includes a "Toggle & Device Availability" note using one of these three patterns:

| Level | Badge Text | What It Means |
|-------|-----------|---------------|
| **Full** | "Available and configurable on all devices (comma 3X/3, comma four, sunnylink)." | The setting appears on every device's screen and in sunnylink. |
| **Config-Hidden** | "Supported on all devices. comma four users must use sunnylink to change this setting." | The feature works on comma four, but the toggle is hidden from the device screen. Use sunnylink to configure it. |
| **Unsupported** | "Supported on: comma 3X/3 only. This feature is currently not available on comma four and cannot be forced via sunnylink." | The feature requires onroad UI rendering code that does not exist on comma four. Forcing the param via sunnylink will not make it work. |

## On-Screen Settings Availability

The table below shows which settings panels have on-screen controls on each platform. A :material-close: means the panel is not shown on that device's screen.

| Panel | comma 3X/3 | comma four | sunnylink |
|-------|:----------:|:----------:|:---------:|
| [Device](device.md) | :material-check: | :material-check: (simplified) | :material-check: |
| [Network](network.md) | :material-check: | :material-check: | :material-check: |
| [sunnylink](sunnylink.md) | :material-check: | :material-close: | :material-check: |
| [Toggles](toggles.md) | :material-check: | :material-check: (fewer items) | :material-check: |
| [Software](software.md) | :material-check: | :material-close: | :material-check: |
| [Models](models.md) | :material-check: | :material-close: | :material-check: |
| [Steering](steering/index.md) | :material-check: | :material-close: | :material-check: |
| [Cruise](cruise/index.md) | :material-check: | :material-close: | :material-check: |
| [Visuals](visuals.md) | :material-check: | :material-close: | :material-check: |
| [Display](display.md) | :material-check: | :material-close: | :material-check: |
| [OSM](osm.md) | :material-check: | :material-close: | :material-check: |
| [Trips](trips.md) | :material-check: | :material-close: | :material-check: |
| [Vehicle](vehicle/index.md) | :material-check: | :material-close: | :material-check: |
| [Firehose](firehose.md) | :material-check: | :material-check: (condensed) | :material-check: |
| [Developer](developer.md) | :material-check: | :material-check: | :material-check: |

## Onroad Visual Features Not Available on comma four

The following features from the [Visuals](visuals.md) panel rely on onroad UI rendering code that only exists on comma 3X/3. These cannot be enabled on comma four:

- Enable Standstill Timer
- Display Road Name
- Green Traffic Light Alert (Beta)
- Lead Departure Alert (Beta)
- Speedometer: Always Display True Speed
- Speedometer: Hide from Onroad Screen
- Display Turn Signals (always-on display; lane change alert icons still appear)
- Real-time Acceleration Bar
- Display Metrics Below Chevron
- Developer UI (onroad overlay)

## What This Means for You

If you use a **comma four**, your on-device screen shows a simplified set of controls. Most sunnypilot features still run on your device - you configure the hidden ones through **sunnylink**. The exception is the onroad visual features listed above, which require rendering code that does not exist on comma four.

If you use a **comma 3X or comma 3**, all settings and onroad visual features are directly accessible from the device sidebar.

!!! tip
    Throughout this manual, each setting includes a "Toggle & Device Availability" note. Look for these callouts to quickly check whether a feature works on your device and where to configure it.
