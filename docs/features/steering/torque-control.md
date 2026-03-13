---
title: Torque Control
---

# Torque Control

## What It Does

Torque Control lets you fine-tune how aggressively or gently sunnypilot steers your vehicle. It provides advanced parameters for lateral acceleration, friction compensation, and self-tuning options.

## How It Works

Torque-based lateral control applies steering commands as torque (rotational force) to the steering motor. The key parameters are:

- **Lateral Acceleration Factor** — How strongly the system turns the wheel (higher = more aggressive)
- **Friction** — How much the system compensates for steering resistance
- **Self-Tune** — Automatically adjusts these values based on your driving

## Requirements

!!! info "Requirements"
    - Vehicle must not use angle-based steering
    - **Enforce Torque Control** must be enabled in [Steering Settings](../../settings/steering/index.md)
    - Mutually exclusive with [NNLC](nnlc.md) — only one can be active at a time
    - Device must be offroad to change settings

## How to Enable

1. Go to **Settings** → **Steering**
2. Enable **Enforce Torque Control**
3. Open the **Torque Settings** sub-panel to fine-tune

## Tuning Options

| Option | Description |
|--------|-------------|
| **Self-Tune** | Automatic real-time parameter adjustment |
| **Relaxed Self-Tune** | Less aggressive auto-tuning for smoother feel |
| **Custom Tune** | Manual parameter override |
| **Lat Accel Factor** | 0.01–5.00 (steering aggressiveness) |
| **Friction** | 0.01–1.00 (friction compensation) |

!!! tip
    Start with Self-Tune enabled. Only switch to Custom Tune if you want precise control over steering feel and are willing to experiment.

## Settings Reference

See [Torque Settings](../../settings/steering/torque.md) for all tuning parameters.
