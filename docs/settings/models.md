---
title: Models Settings
---

# Models Settings

Select and manage driving models, and configure model-related parameters.

**Location**: `Settings -> Models`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Current Model

A button labeled **SELECT** that opens a model selection dialog. The currently active model name is displayed. Choose from available driving models, each with different driving characteristics and capabilities.

!!! warning "Offroad Only"
    Model selection can only be changed while the vehicle is offroad (parked with ignition off), unless Always Offroad mode is active.

---

## Model Download Progress

When a model is being downloaded, progress bars appear for each component:

- **Driving Model** - the main supercombo neural network
- **Vision Model** - the vision processing model
- **Policy Model** - the decision-making policy model

Each shows a progress bar with download percentage.

---

## Refresh Model List

A button that forces a refresh of the available model list from the server. Use this if you expect a new model to be available but do not see it in the selection dialog.

---

## Clear Model Cache

A button that deletes all downloaded models except the currently active one. The current cache size in MB is displayed. Useful for freeing storage space.

---

## Cancel Download

A button that appears only while a model download is in progress. Cancels the current download.

---

## Use Lane Turn Desires

When enabled, at speeds of 20 mph (32 km/h) or below with the turn signal on, the model plans a turn in the blinker direction at the nearest drivable path. This helps the model make smoother turns at low speeds.

---

## Adjust Lane Turn Speed

A selector that sets the maximum speed at which lane turn desires are active. Default is 19 mph. Use the **-** and **+** buttons to adjust.

!!! note "Availability"
    Only appears when **Use Lane Turn Desires** is enabled and **Show Advanced Controls** is enabled in [Developer Settings](developer.md).

---

## Live Learning Steer Delay

Enables real-time learning and adaptive steering response time. The system continuously measures the actual steering delay and adjusts compensation accordingly. When disabled, a fixed response time is used instead.

The description text shows the current live delay value or a breakdown of delay components.

---

## Adjust Software Delay

A selector that sets the fixed software delay value used when Live Learning Steer Delay is disabled. Default is 0.2 seconds. Use the **-** and **+** buttons to adjust.

!!! note "Availability"
    Only appears when **Live Learning Steer Delay** is disabled and **Show Advanced Controls** is enabled in [Developer Settings](developer.md).
