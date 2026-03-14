---
title: Device Settings
---

# Device Settings

View device information, manage calibration, configure power behavior, and access system utilities.

**Location**: `Settings -> Device`

!!! info "Toggle & Device Availability"
    Available and configurable on all devices (comma 3X/3, comma four, sunnylink).

---

## Device Information

The top of the panel displays your device's **Dongle ID** and **Serial** number. These identifiers are used for pairing and support.

---

## Pair Device

Pairs your comma device with your comma connect account. Once paired, you can view driving routes, manage the device remotely, and access dashcam footage through the comma connect app.

---

## Reset Calibration

Resets the device's calibration data. After reset, the system will re-learn the camera's mounting position during your next drive. The current calibration status is shown in the description text.

---

## Change Language

Opens a language selection dialog where you can choose the display language for the interface.

---

## Enable Always Offroad / Exit Always Offroad

Toggles "Always Offroad" mode. When enabled, the device stays in its offroad (parked) state even when the vehicle is running. This prevents the driving assist from engaging, so you can configure settings, download updates, or perform maintenance without the system attempting to control the vehicle.

The button text and color change based on the current state:

- **"Enable Always Offroad"** — shown when the mode is off
- **"Exit Always Offroad"** — shown when the mode is active

A confirmation dialog appears before toggling.

!!! note "Availability"
    This button is only available while the device is offroad (parked). See [Wake Up Behavior](#wake-up-behavior) to have the device start in Always Offroad mode automatically.

---

## Wake Up Behavior

A row of two buttons that controls what the device does when it boots or wakes from sleep:

| Option | What it does |
|--------|-------------|
| **Default** | Device boots normally and is ready to engage |
| **Offroad** | Device automatically enables [Always Offroad](#enable-always-offroad--exit-always-offroad) on each boot or wake-up |

When set to **Offroad**, the device sets Always Offroad mode every time it starts — the driving assist will not engage until you manually exit Always Offroad from the Device settings panel. This is useful if you want the device to stay in a configuration or maintenance state by default.

This setting persists across reboots. The resulting Always Offroad state, however, is transient: it is re-applied on each boot by this setting rather than carried over from the previous session.

---

## Max Time Offroad

A selector that sets how long the device stays powered on after the engine is turned off before automatically shutting down. The default is **30 hours**.

Available options: **Always On**, **5m**, **10m**, **15m**, **30m**, **1h**, **2h**, **3h**, **5h**, **10h**, **24h**, **30h**

Setting this to **Always On** disables the auto-shutdown timer entirely — the device will stay on until manually powered off or until battery voltage drops too low.

---

## Quiet Mode

Toggles quiet mode on or off. When enabled, the device suppresses non-critical sounds while preserving all safety-related alerts. This setting can be toggled while driving.

**Alerts that always play** (even in Quiet Mode):

- Soft warnings (`warningSoft`)
- Immediate warnings (`warningImmediate`)
- Driver distraction prompts (`promptDistracted`)
- Repeated attention prompts (`promptRepeat`)

**Alerts that are muted** in Quiet Mode:

- Engagement sound
- Disengagement sound
- Refusal sound
- Standard prompts

---

## Driver Camera Preview

Opens a live preview of the driver-facing camera so you can verify its position and angle.

!!! note "Availability"
    Disabled while the vehicle is onroad.

---

## Onroad Uploads

Toggles data uploads while driving. Enabled by default.

When enabled, the device uploads driving segments over a cellular or Wi-Fi connection during your drive. When disabled, uploads are deferred until the vehicle is parked and the device is offroad.

Disabling this is useful if you are on a metered or limited data connection (for example, a mobile hotspot used for navigation or OSM-based features) and want to conserve bandwidth while driving.

---

## Training Guide

Opens the sunnypilot training guide, which walks through the system's rules, features, and limitations.

!!! note "Availability"
    Disabled while the vehicle is onroad.

---

## Regulatory

Displays FCC regulatory information for the device.

!!! note "Availability"
    Disabled while the vehicle is onroad.

---

## Reset Settings

Resets all sunnypilot settings to their defaults. This is a two-step confirmation to prevent accidental resets. After confirmation, the device reboots.

!!! warning
    This action cannot be undone. All custom settings will be lost.

!!! note "Availability"
    Disabled while the vehicle is onroad.

---

## Reboot / Power Off

**Reboot** restarts the device. **Power Off** shuts the device down completely.

Power Off is hidden while the vehicle is onroad to prevent accidental shutdown during driving.

---

## Platform Differences

On **comma four**, the Device panel has a simplified layout with these items:

- Device ID and Serial (info display)
- Update sunnypilot
- Pair
- Review Training Guide
- Driver Camera Preview
- Terms & Conditions
- Regulatory Info
- Reset Calibration
- Uninstall sunnypilot
- Reboot / Power Off (circle buttons)

The comma four panel does not include: Always Offroad, Wake Up Behavior, Max Time Offroad, Quiet Mode, Onroad Uploads, Reset Settings, or Change Language.
