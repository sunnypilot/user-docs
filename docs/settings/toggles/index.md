---
title: Toggles
---

# Toggles

Core driving assist toggles that control fundamental sunnypilot behavior, driving personality, driver monitoring, and data recording.

**Location**: `Settings -> Toggles`

!!! info "Toggle & Device Availability"
    Available and configurable on all devices (comma 3X/3, comma four, sunnylink).

---

## Enable sunnypilot

Enables the sunnypilot driving assist system for adaptive cruise control and lane keeping. Your attention is required at all times while the system is active.

!!! warning "Restart Required"
    Changing this toggle requires the device to be offroad (parked, ignition off). A restart is needed for the change to take effect.

---

## Experimental Mode

Activates end-to-end longitudinal control with a new driving visualization. This alpha feature uses the neural network to handle gas and braking on all road types, including city streets with stop signs and traffic lights.

!!! note "Availability"
    Requires longitudinal control. Not available on vehicles using stock adaptive cruise control.

---

## Disengage on Accelerator Pedal

When enabled, pressing the gas pedal will immediately disengage sunnypilot. When disabled, pressing the gas pedal overrides sunnypilot's speed control without disengaging the system.

---

## Driving Personality

A row of three buttons that controls how closely sunnypilot follows the vehicle ahead and how aggressively it accelerates and brakes:

| Personality | Behavior |
|-------------|----------|
| **Aggressive** | Shorter following distance, quicker acceleration |
| **Standard** | Moderate following distance and response |
| **Relaxed** | Longer following distance, gentler acceleration |

!!! note "Availability"
    Requires longitudinal control.

---

## Enable Lane Departure Warnings

Alerts you to steer back into your lane when the vehicle drifts over a detected lane line without the turn signal active. Warnings activate above 31 mph (50 km/h).

---

## Always-On Driver Monitoring

Keeps the driver monitoring camera active even when sunnypilot is not engaged. The system will still watch for distracted or drowsy driving whenever the vehicle is on.

---

## Record and Upload Driver Camera

Uploads footage from the driver-facing camera to help improve the driver monitoring algorithm. When enabled, driver camera data is included in uploaded driving segments.

!!! warning "Restart Required"
    Changing this toggle requires the device to be offroad.

---

## Record and Upload Microphone Audio

Records microphone audio while driving. The audio is stored locally and included in dashcam video available through comma connect.

!!! warning "Restart Required"
    Changing this toggle requires the device to be offroad.

---

## Use Metric System

Switches the display from miles per hour (mph) to kilometers per hour (km/h) throughout the interface.

---

## Platform Differences

On **comma four**, this panel contains the same toggles with slightly different labels:

| comma 3X/3 Label | comma four Label |
|-------------------|-----------------|
| Enable sunnypilot | enable sunnypilot |
| Driving Personality | driving personality |
| Experimental Mode | experimental mode |
| Use Metric System | use metric units |
| Enable Lane Departure Warnings | lane departure warnings |
| Always-On Driver Monitoring | always-on driver monitor |
| Record and Upload Driver Camera | record & upload driver camera |
| Record and Upload Microphone Audio | record & upload mic audio |
