---
title: Software Settings
---

# Software Settings

Manage software updates, view release notes, and switch branches.

**Location**: `Settings -> Software`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Current Version

Displays the currently installed version of sunnypilot. The description text shows release notes for the current version.

---

## Download

A button that checks for available updates. If an update is found, the button changes to **DOWNLOAD** to begin downloading. Progress is shown during the download.

!!! note "Availability"
    Only available while the device is offroad.

---

## Install Update

A button that appears after an update has been downloaded. Tapping it reboots the device to install the update.

!!! note "Availability"
    Only appears when an update has been downloaded and the device is offroad.

---

## Target Branch

A button labeled **SELECT** that opens a branch selection dialog. Choose which sunnypilot branch to track for updates. The currently selected branch is displayed.

!!! tip
    For daily driving, stay on the latest **release** branch. Switch to staging or dev branches only if you want to test new features.

---

## Uninstall

A button that uninstalls sunnypilot from the device. Requires confirmation before proceeding.

---

## Disable Updates

Prevents the device from checking for or applying software updates. The device remains on its current version indefinitely. A reboot prompt appears when toggling this setting.

!!! note "Availability"
    Only appears when **Show Advanced Controls** is enabled in [Developer Settings](developer.md). Can only be changed while the device is offroad.
