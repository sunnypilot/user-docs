---
title: GM / Chevrolet Settings
---

# GM / Chevrolet Vehicle Settings

Information about sunnypilot behavior on GM and Chevrolet vehicles. These notes apply when a GM or Chevrolet vehicle is connected or selected.

**Location**: `Settings -> Vehicle`

---

## Non-ACC Vehicle Support

sunnypilot supports certain GM vehicles that lack factory Adaptive Cruise Control (ACC). On these vehicles, cruise control state is read from the Engine Control Module (ECM) instead of the ACC module. This enables steering-only assistance on platforms that would otherwise be unsupported.

---

## Steering Torque Models

sunnypilot uses vehicle-specific steering torque models to optimize lateral control for GM vehicles:

| Vehicle | Model Type | Description |
|---------|-----------|-------------|
| Bolt EUV | Neural network feedforward | A 4-layer neural network that provides precise steering response |
| Bolt EUV, Acadia, Silverado | Sigmoid-linear (SigLin) | A non-linear torque curve that reduces steering noise on straight roads while maintaining responsiveness in turns |
| Other GM vehicles | Linear | Standard linear torque mapping |

These models are applied automatically based on your vehicle — no configuration is needed.
