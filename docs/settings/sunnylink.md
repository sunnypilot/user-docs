---
title: sunnylink Settings
---

# sunnylink Settings

Configure the sunnylink cloud integration for secure backup, restore, sponsorship, and remote configuration.

**Location**: `Settings -> sunnylink`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Enable sunnylink

Master toggle for all sunnylink features. When disabled, no sunnylink requests are made. Your Dongle ID is displayed next to the toggle.

Enabling sunnylink for the first time triggers a consent prompt that must be completed before the feature activates.

!!! note "Availability"
    Can only be changed while the device is offroad.

---

## Sponsor Status

A button that opens the sponsor status dialog. Displays your current sponsor tier name and color. Becoming a sponsor grants early access to sunnylink features.

!!! note "Availability"
    Disabled when sunnylink is not enabled.

---

## Pair GitHub Account

A button that opens the GitHub pairing dialog. Links your GitHub account to the device for sponsor verification and API access. Displays **Paired** or **Not Paired** as the current status.

!!! note "Availability"
    Disabled when sunnylink is not enabled.

---

## Enable sunnylink uploader (infrastructure test)

Uploads driving data to sunnypilot servers. This feature is currently available to highest-tier sponsors only and is used for testing data volume and upload infrastructure.

!!! note "Availability"
    Disabled when sunnylink is not enabled.

---

## Backup Settings / Restore Settings

Two side-by-side buttons for managing settings backups through sunnylink:

- **Backup Settings**: Encrypts and uploads all current sunnypilot settings to the cloud. A progress indicator shows the upload status.
- **Restore Settings**: Downloads and applies the most recently backed-up settings. A progress indicator shows the download status.

!!! note "Availability"
    Both buttons are disabled while the device is onroad or when sunnylink is not enabled.

---

## Related Features

- [sunnylink](../features/connected/sunnylink.md)
