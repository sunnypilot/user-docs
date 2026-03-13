---
title: Neural Network Lateral Control
---

# Neural Network Lateral Control (NNLC)

## What It Does

NNLC replaces the traditional PID or torque-based steering controller with a neural network trained on real driving data. This can provide smoother, more natural-feeling lane keeping that adapts to your vehicle's steering characteristics.

## How It Works

Instead of using fixed mathematical formulas (PID controller), NNLC uses a machine learning model to calculate steering commands. The neural network has been trained on real-world driving data and can handle a wider variety of driving scenarios with smoother output.

!!! note "Evolution from NNFF"
    NNLC evolved from **Neural Network FeedForward (NNFF)**, an earlier approach that used a neural network as a feedforward component alongside traditional controllers. NNLC builds on this foundation by giving the neural network full lateral control authority, resulting in improved steering smoothness and adaptability.

!!! info "Vehicle-Specific Training Data"
    The neural network models are trained on real driving data collected from specific vehicles. Because each vehicle has unique steering characteristics, a dedicated model must be trained for each supported make/model. Over **70 vehicle models** currently have trained NNLC models available. If no model exists for your vehicle, the NNLC toggle will not appear in settings.

### Model Matching

When NNLC is enabled, the system matches your vehicle to the best available model using a 3-tier fallback:

| Tier | Match Criteria | Confidence | Description |
|------|---------------|------------|-------------|
| **1. Exact** | Fingerprint + firmware version | ≥ 0.99 | Best match — a model trained on your exact vehicle and firmware combination |
| **2. Valid** | Fingerprint only | ≥ 0.9 | Good match — a model trained on your vehicle platform, regardless of firmware version |
| **3. Substitute** | Substitute table lookup | Fallback | A model from a similar vehicle platform is used as a substitute (configured in `substitute.toml`) |

## Requirements

!!! info "Requirements"
    - Vehicle must not use angle-based steering (`steerControlType` must not be `angle`)
    - A trained NNLC model must be available for your specific vehicle
    - Mutually exclusive with [Torque Control](torque-control.md) — only one can be active at a time
    - Device must be offroad to enable/disable

## How to Enable

**Settings** → **Steering** → **Neural Network Lateral Control**

!!! tip
    Not all vehicles have NNLC models available. If the toggle does not appear, your vehicle may use angle-based steering which is not compatible with NNLC, or a trained model may not yet exist for your vehicle.

## NNLC vs. Torque Control

| Feature | NNLC | Torque Control |
|---------|------|---------------|
| **Approach** | Neural network (learned) | Mathematical formula (tuned) |
| **Customization** | Automatic | Manual tuning available |
| **Best for** | Smooth, adaptive steering | Precise, configurable steering |

These two features are mutually exclusive — enabling one automatically disables the other.

## Settings Reference

See [Steering Settings](../../settings/steering/index.md) for configuration details.
