---
title: Visuals Settings
---

# Visuals Settings

Configure what information and visual elements appear on the driving screen.

**Location**: `Settings -> Visuals`

!!! info "Toggle & Device Availability"
    This panel contains a mix of features. Some work on all devices, while others require onroad UI elements that only exist on comma 3X/3. Each item below includes its own availability note.

---

## Show Blind Spot Warnings

Displays visual warnings on the driving screen when a vehicle is detected in your blind spot. Only available on vehicles equipped with Blind Spot Monitoring (BSM) hardware.

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Steering Arc

Shows the steering arc overlay on the driving screen when lateral (steering) control is active. This arc illustrates the path sunnypilot is steering toward.

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting. Note: On comma four, the steering arc is always displayed and cannot be toggled off.

---

## Enable Tesla Rainbow Mode

Applies a rainbow color effect to the model's planned driving path displayed on screen. This is a cosmetic change only and does not affect driving behavior.

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Enable Standstill Timer

Displays a timer on the HUD when the vehicle is stopped. The timer shows how long you have been at a standstill.

!!! info "Toggle & Device Availability"
    Supported on: comma 3X/3 only. This feature is currently not available on comma four and cannot be forced via sunnylink.

---

## Display Road Name

Shows the name of the road you are currently driving on. Requires the OSM map database to be downloaded through the [OSM panel](osm.md).

!!! info "Toggle & Device Availability"
    Supported on: comma 3X/3 only. This feature is currently not available on comma four and cannot be forced via sunnylink.

---

## Green Traffic Light Alert (Beta)

Plays a chime and shows an on-screen alert when the traffic light ahead turns green while you are stopped with no lead vehicle in front. Helps you notice the light change.

!!! info "Toggle & Device Availability"
    Supported on: comma 3X/3 only. This feature is currently not available on comma four and cannot be forced via sunnylink.

---

## Lead Departure Alert (Beta)

Plays a chime and shows an on-screen alert when you are stopped and the vehicle ahead begins moving. Useful for noticing when traffic starts flowing again.

!!! info "Toggle & Device Availability"
    Supported on: comma 3X/3 only. This feature is currently not available on comma four and cannot be forced via sunnylink.

---

## Speedometer: Always Display True Speed

Forces the speedometer to always show the true vehicle speed from wheel speed sensors, rather than the GPS-based speed. Applicable to vehicles where wheel speed and GPS speed differ.

!!! info "Toggle & Device Availability"
    Supported on: comma 3X/3 only. This feature is currently not available on comma four and cannot be forced via sunnylink.

---

## Speedometer: Hide from Onroad Screen

Hides the speedometer from the driving screen entirely. When enabled, no speed is displayed while driving.

!!! info "Toggle & Device Availability"
    Supported on: comma 3X/3 only. This feature is currently not available on comma four and cannot be forced via sunnylink.

---

## Display Turn Signals

Draws visual turn signal indicators on the HUD when the turn signals are active.

!!! info "Toggle & Device Availability"
    Supported on: comma 3X/3 only. This feature is currently not available on comma four and cannot be forced via sunnylink. Note: On comma four, turn signal icons appear during lane change alerts only, but the always-on display does not exist.

---

## Real-time Acceleration Bar

Shows a vertical bar on the left side of the driving screen that indicates real-time acceleration and deceleration. The bar moves up during acceleration and down during braking.

!!! info "Toggle & Device Availability"
    Supported on: comma 3X/3 only. This feature is currently not available on comma four and cannot be forced via sunnylink.

---

## Display Metrics Below Chevron

A row of five buttons that controls what information appears below the lead vehicle chevron on the driving screen:

| Option | What it shows |
|--------|--------------|
| **Off** | Nothing displayed below the chevron |
| **Distance** | Distance to the lead vehicle |
| **Speed** | Speed of the lead vehicle |
| **Time** | Time gap to the lead vehicle |
| **All** | Distance, speed, and time together |

!!! note "Availability"
    Requires sunnypilot longitudinal control.

!!! info "Toggle & Device Availability"
    Supported on: comma 3X/3 only. This feature is currently not available on comma four and cannot be forced via sunnylink.

---

## Developer UI

A row of four buttons that controls the display of real-time developer metrics on the driving screen:

| Option | What it shows |
|--------|--------------|
| **Off** | No developer information displayed |
| **Bottom** | Metrics displayed at the bottom of the screen |
| **Right** | Metrics displayed on the right side |
| **Right & Bottom** | Metrics displayed on both the right side and bottom |

!!! info "Toggle & Device Availability"
    Supported on: comma 3X/3 only. This feature is currently not available on comma four and cannot be forced via sunnylink.

---

## Related Features

- [HUD & Visuals](../features/display/hud-visuals.md)
