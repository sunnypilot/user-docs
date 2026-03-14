---
title: Firehose Settings
---

# Firehose Settings

Firehose Mode uploads training data from your drives to comma's servers, helping improve autonomous driving models.

**Location**: `Settings -> Firehose`

!!! info "Toggle & Device Availability"
    Available and configurable on all devices (comma 3X/3, comma four, sunnylink).

!!! info "First Fork with Official Support"
    sunnypilot is the first and currently only major fork to receive official Firehose Mode support.

---

## How It Works

When Firehose Mode is active, the system randomly samples a portion of your drives rather than uploading everything. It queues approximately 10 segments at a time for transmission, whether sunnypilot is actively engaged or not. Both engaged and disengaged driving data contributes to simulator training.

No special driving behavior is needed. Normal driving patterns work fine.

---

## Status Display

The panel shows whether Firehose Mode is currently active or inactive:

- **Active** (green): The device is connected to an unmetered network and uploading data.
- **Inactive** (red): Connect to an unmetered Wi-Fi network to begin uploading.

If available, the panel also displays the number of segments you have contributed to the training dataset.

---

## Requirements

- **Compatible branch**: You must be running one of the following branches:
    - `staging`, `dev`, or `master`
    - `staging-tici`, `master-tici`
    - `release-tizi` or `release-tici`
- **Weekly connectivity**: Connect to Wi-Fi with a reliable USB-C power adapter at minimum once per week.
- **Supported vehicle**: Only vehicles officially supported in upstream openpilot qualify for model training data collection.

---

## Optional: Mobile Upload

Devices with hotspot access or unlimited data plans can upload data while driving, removing the need for weekly Wi-Fi sessions.
