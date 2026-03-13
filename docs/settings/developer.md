---
title: Developer Settings
---

# Developer Settings

Advanced settings for developers and power users, including debug tools, connectivity options, and alpha features.

**Location**: `Settings -> Developer`

!!! info "Toggle & Device Availability"
    Available and configurable on all devices (comma 3X/3, comma four, sunnylink).

---

## Show Advanced Controls

Reveals additional advanced settings throughout the sunnypilot interface. Enabling this does not change any driving behavior - it only makes hidden controls visible.

Settings gated behind this toggle include:

- [Models](models.md): Adjust Lane Turn Speed, Adjust Software Delay
- [Software](software.md): Disable Updates
- Developer: GitHub Runner Service, copyparty Service, Quickboot Mode

---

## Enable ADB

Enables ADB (Android Debug Bridge) for connecting to the device over USB or network for debugging.

!!! note "Availability"
    Can only be changed while the device is offroad.

---

## Enable SSH

Enables SSH access to the device for remote terminal sessions.

---

## SSH Keys

A button that fetches SSH public keys from a GitHub username and installs them on the device. This allows SSH login using your GitHub-associated key pair.

!!! warning
    Only add SSH keys from users you trust. Anyone with an installed key has full access to the device.

---

## Joystick Debug Mode

Enables joystick-controlled driving for testing and development purposes.

!!! note "Availability"
    Hidden on release branches. Can only be changed while the device is offroad.

---

## Longitudinal Maneuver Mode

Enables a longitudinal debug mode for testing acceleration and braking maneuvers.

!!! note "Availability"
    Hidden on release branches. Requires longitudinal control and the device must be offroad.

---

## sunnypilot Longitudinal Control (Alpha)

Enables alpha-quality longitudinal control for vehicles that do not yet have full upstream support. This replaces the car's stock adaptive cruise control with sunnypilot's own gas and brake management.

!!! warning
    Enabling this disables AEB (Automatic Emergency Braking). A confirmation dialog appears before activation.

!!! note "Availability"
    Hidden on release branches. Only appears if your vehicle supports alpha longitudinal control.

---

## UI Debug Mode

Shows touch indicators, FPS counter, and mouse coordinates on screen. Useful for UI development and troubleshooting display issues.

---

## GitHub Runner Service

Enables the GitHub Actions self-hosted runner service on the device. This allows the device to execute CI/CD jobs from your repository.

!!! note "Availability"
    Only appears when **Show Advanced Controls** is enabled. Hidden on release branches.

---

## copyparty Service

Enables a file server on the device for downloading driving routes and logs from a web browser via the device's local IP address.

!!! note "Availability"
    Only appears when **Show Advanced Controls** is enabled.

---

## Quickboot Mode

Creates a prebuilt file for accelerated boot, reducing startup time. Requires software updates to be disabled first.

!!! note "Availability"
    Only appears when **Show Advanced Controls** is enabled, the device is not on a release or development branch, and **Disable Updates** is enabled in [Software Settings](software.md).

---

## Error Log

A **VIEW** button that opens the sunnypilot crash error log in a viewer. On close, you are offered the option to delete the log.

!!! note "Availability"
    Hidden on release branches.

---

## Platform Differences

On **comma four**, the Developer panel includes:

- ADB (circle icon toggle)
- SSH (circle icon toggle)
- SSH Keys
- Joystick Debug Mode
- Longitudinal Maneuver Mode
- Alpha Longitudinal
- UI Debug Mode

The comma four panel does not include: Show Advanced Controls, GitHub Runner Service, copyparty Service, Quickboot Mode, or Error Log.
