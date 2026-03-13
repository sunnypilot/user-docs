---
title: sunnylink
---

# sunnylink

## What It Does

sunnylink is sunnypilot's cloud backend integration system. It connects your device to the sunnypilot cloud infrastructure, enabling settings backup and restore, sponsor benefits, remote device management, and optional driving data uploads.

## Key Features

### Settings Backup & Restore

Securely back up your device configuration to the cloud and restore it on the same or a different device.

- **Backup** compresses and encrypts all your sunnypilot settings using AES-256-CBC encryption derived from your device's unique RSA key
- **Restore** downloads and decrypts your backup, applying only recognized sunnypilot parameters
- Progress is displayed in real-time (0-100%) during both operations
- Backups include all sunnypilot-specific parameters (toggles, tuning values, preferences)

!!! note
    Backups are device-key encrypted. A backup created on one device can only be restored to the same device or by using the same device keys.

### Sponsor Tiers

sunnylink has a sponsorship system with multiple tiers:

| Tier | Color |
|------|-------|
| Guardian | Gold |
| Benefactor | Green |
| Contributor | Steel Blue |
| Supporter | Purple |
| Free / Novice | Default |

Sponsor status is displayed in the sunnylink settings panel. Higher tiers may unlock additional features (such as the infrastructure uploader).

### GitHub Account Pairing

Link your GitHub account to your device for sponsor verification and identity management. The pairing status is displayed in the sunnylink settings panel as "Paired" or "Not Paired".

### Data Upload (Infrastructure Test)

When enabled, sunnylink can upload driving logs and camera data to sunnypilot's cloud infrastructure. This feature prioritizes crash and boot logs, respects metered connections (skips video on cellular), and uses signed S3 URLs for secure uploads.

!!! warning
    The uploader is currently an infrastructure test feature available to high-tier sponsors only. It provides no direct user benefit at this time.

### Remote Device Management

sunnylink maintains a persistent WebSocket connection to the backend, enabling:

- Remote parameter viewing and modification
- Log upload control
- Local port proxying for SSH-like access
- Queued message processing

## How to Configure

**Settings** → **sunnylink**

sunnylink requires explicit user consent before activation. On first enable, a consent dialog explains what data is collected and how it is used.

## Settings Reference

See [sunnylink Settings](../../settings/sunnylink.md) for all configuration options.
