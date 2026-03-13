---
title: Dynamic Experimental Control
---

# Dynamic Experimental Control (DEC)

## What It Does

DEC automatically switches between openpilot's two longitudinal modes based on real-time road conditions. Instead of manually toggling between modes, the system dynamically selects the most appropriate mode for the current situation.

To understand DEC, it helps to know the two driving modes it switches between:

| Mode | Internal Name | Description |
|------|---------------|-------------|
| **Chill / Standard** | `acc` | The default openpilot driving mode. Follows the lead car and stays in lane at a steady speed. Best suited for highway and open-road driving where stops and complex maneuvers are rare. |
| **Experimental** | `blended` | An enhanced mode that uses the end-to-end (E2E) driving model. Can handle stops at traffic lights and stop signs, navigate turns, and respond to more complex urban scenarios. Designed for city driving. |

!!! note "DEC is a switcher, not a mode"
    DEC is not a third driving mode — it is a dynamic switcher that automatically selects between `acc` (Chill/Standard) and `blended` (Experimental) in real time based on road conditions.

## How It Works

DEC uses a confidence-based switching system with specific probability thresholds and hysteresis to prevent rapid mode toggling:

### Detection Signals

| Signal | Threshold | Effect |
|--------|-----------|--------|
| **Lead vehicle probability** | ≥ 0.45 | Favors `acc` mode (standard following) |
| **Slow-down probability** | ≥ 0.3 | Favors `blended` mode (E2E for stops/turns) |
| **Stop sign / traffic light** | Detected by vision model | Triggers switch to `blended` mode |
| **Turn detection** | Upcoming turns | Triggers switch to `blended` mode |
| **Current speed** | Speed-dependent | Lower speeds favor `blended` mode |

### Switching Logic

- DEC uses **Kalman filters** to smooth probability signals and reduce noise
- A **minimum hold time of 10 frames** prevents rapid oscillation between modes
- A **confidence threshold of 0.6** must be met before switching to a new mode
- The system continuously evaluates conditions and transitions seamlessly without driver input

Based on these signals, DEC switches between:

| Mode | When DEC Activates It |
|------|----------|
| **Chill / Standard** (`acc`) | Highway driving with steady speeds, lead vehicle following, clear lanes, and no upcoming stops or complex intersections |
| **Experimental** (`blended`) | City driving with stops, turns, traffic lights, and complex intersections where the vehicle needs to slow down or stop |

## Requirements

!!! info "Requirements"
    - Longitudinal control must be available
    - Device must be offroad to enable/disable

## How to Enable

**Settings** → **Cruise** → **Dynamic Experimental Control**

## Settings Reference

See [Cruise Control Settings](../../settings/cruise/index.md) for configuration details.
