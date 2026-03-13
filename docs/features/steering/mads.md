---
title: Modular Assistive Driving System
---

# Modular Assistive Driving System (MADS)

## What It Does

MADS decouples lateral (steering) and longitudinal (speed) controls. In standard openpilot, engaging cruise control activates both steering and speed control together, and disengaging turns both off. With MADS, steering assistance can remain active independently — even when cruise control is off.

This means you can have lane-keeping assistance while controlling the gas and brakes yourself.

## How It Works

With MADS enabled, Automatic Lane Centering (ALC) and Adaptive Cruise Control (ACC) can be engaged and disengaged independently. This is the core difference from standard openpilot, where both are always linked together.

- **Steering stays active** even when you cancel cruise control — ALC continues to provide lane centering while you control speed manually
- **Independent engagement** — you can activate ALC without ACC, or both together, giving you flexible control over which assists are active
- You choose what happens to steering when cruise disengages (remain active, pause, or fully disengage)
- You can configure whether the main cruise button also activates steering

### Engagement States

MADS has five internal states:

| State | Description |
|-------|-------------|
| **Disabled** | MADS is off — no steering assistance is provided |
| **Enabled** | Steering assistance is fully engaged and actively providing lane centering |
| **Paused** | Steering assistance is temporarily paused (e.g., due to braking, depending on your Steering Mode on Brake setting) but can resume without re-engaging |
| **Soft Disabling** | The system is transitioning from enabled to disabled due to a safety condition (e.g., driver inattention alert escalation) |
| **Overriding** | The driver is actively steering, temporarily overriding the system's lateral input. Steering assistance resumes when the driver releases the wheel |

### Steering Mode on Brake

This setting controls what happens to steering assistance when the brake pedal is pressed:

| Option | Value | Behavior |
|--------|-------|----------|
| **Remain Active** | 0 | Steering stays fully active while braking |
| **Pause** | 1 | Steering pauses while braking, resumes on release |
| **Disengage** | 2 | Steering fully disengages on brake — must re-engage manually |

## Requirements

!!! info "Requirements"
    - Supported on most vehicles with sunnypilot lateral control

## How to Enable

**Settings** → **Steering** → enable **MADS**

Then configure the sub-settings in **MADS Settings**.

## Key Settings

| Setting | What It Controls |
|---------|-----------------|
| **Main Cruise Allowed** | Whether the cruise on/off button can activate MADS |
| **Unified Engagement Mode** | Whether engaging cruise also engages MADS automatically |
| **Steering Mode on Brake** | What happens to steering when the brake is pressed (Remain Active / Pause / Disengage) |
| **Steering Mode on Disengage** | What happens to steering when cruise disengages |

## Vehicle-Specific Behavior

Some vehicles operate in **limited MADS mode** where certain settings are locked due to platform constraints (e.g., no vehicle bus access):

=== "Tesla (without vehicle bus)"
    - Main Cruise Allowed: forced OFF
    - Unified Engagement Mode: forced ON
    - Steering Mode on Brake: forced to **Disengage**

=== "Rivian"
    - Main Cruise Allowed: forced OFF
    - Unified Engagement Mode: forced ON
    - Steering Mode on Brake: forced to **Disengage**

!!! note "Why these restrictions?"
    Vehicles without a full vehicle bus connection (like Tesla without the vehicle bus harness and Rivian) cannot reliably detect certain driver inputs. To maintain safety, MADS defaults to the most conservative behavior on these platforms.

## Settings Reference

See [MADS Settings](../../settings/steering/mads.md) for all configuration options.

!!! warning "Safety"
    Always be ready to take full manual control. MADS allows more flexible use of driver assistance, but you remain responsible for safe driving at all times.
