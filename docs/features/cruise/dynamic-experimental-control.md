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

DEC derives its signals from model trajectory analysis and Kalman-filtered state estimates:

| Signal | Threshold | Effect |
|--------|-----------|--------|
| **Lead vehicle detection** | Filtered confidence ≥ 0.45 | Favors `acc` mode (standard following) |
| **Slow-down detection** | Filtered urgency ≥ 0.3 | Favors `blended` mode (the model's predicted trajectory endpoint is closer than expected, indicating a stop or slowdown ahead) |
| **Current speed** | Speed-dependent | Lower speeds favor `blended` mode |
| **Standstill** | Vehicle stopped | Evaluated for mode hold |

!!! note
    DEC does not use separate stop sign, traffic light, or turn classifiers. It infers all stop/slowdown scenarios from the model's trajectory endpoint distance relative to expected travel distance. The system also distinguishes between radar and radarless vehicles, using different decision logic for each.

### Switching Logic

- DEC uses **Kalman filters** to smooth probability signals and reduce noise
- A **minimum hold time of 10 frames** prevents rapid oscillation between modes
- A **confidence threshold of 0.6** must be met before switching to a new mode
- The system continuously evaluates conditions and transitions seamlessly without driver input

Based on these signals, DEC switches between:

| Mode | When DEC Activates It |
|------|----------|
| **Chill / Standard** (`acc`) | Highway driving with steady speeds, lead vehicle following, and no predicted slowdown ahead |
| **Experimental** (`blended`) | Situations where the model predicts the vehicle needs to slow down or stop ahead (intersections, turns, traffic) |

## Requirements

!!! info "Requirements"
    - Longitudinal control must be available

## How to Enable

**Settings** → **Cruise** → **Dynamic Experimental Control**

## Settings Reference

See [Cruise Control Settings](../../settings/cruise/index.md) for configuration details.
