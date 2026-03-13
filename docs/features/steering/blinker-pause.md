---
title: Blinker Pause Lateral Control
---

# Blinker Pause Lateral Control

## What It Does

Temporarily pauses lateral (steering) control when you activate a turn signal. This gives you full manual steering control during the blinker activation, useful for situations where you want to make a manual lane adjustment or turn without the system fighting your steering input.

## How It Works

1. You activate a turn signal (left or right blinker)
2. If your speed is **below** the configured speed threshold, sunnypilot pauses lateral control
3. Lateral control stays paused while the blinker is active
4. After the blinker is deactivated, lateral control re-engages after the configured delay

## Configuration Options

### Speed Threshold

The maximum speed at which Blinker Pause activates. Above this speed, lateral control remains active even with the blinker on (this allows Auto Lane Change to work at highway speeds).

### Re-Engage Delay

How long after the blinker is deactivated before lateral control re-engages. A short delay prevents abrupt steering corrections immediately after turning off the signal.

## How to Configure

**Settings** → **Steering**

Look for the Blinker Pause Lateral Control toggle and its sub-settings.

## Settings Reference

See [Steering Settings](../../settings/steering/index.md) for all configuration options.
