---
title: GM / Chevrolet Settings
---

# GM / Chevrolet Vehicle Settings

Information about sunnypilot behavior on GM and Chevrolet vehicles. These notes apply when a GM or Chevrolet vehicle is connected or selected.

**Location**: `Settings -> Vehicle`

---

## Non-ACC Vehicle Support

sunnypilot supports certain GM vehicles that lack factory Adaptive Cruise Control (ACC). On these vehicles, cruise control state is read from the Engine Control Module (ECM) instead of the ACC module. This enables steering-only assistance on platforms that would otherwise be unsupported.

Supported Non-ACC vehicles:

- Chevrolet Bolt 2017
- Chevrolet Bolt 2018-21
- Chevrolet Bolt EUV/EV 2022-23
- Chevrolet Equinox 2019-22
- Chevrolet Suburban 2016-20
- Cadillac CT6 2017-18
- Chevrolet Trailblazer 2021-22
- Chevrolet Malibu 2016-23
- Cadillac XT5 2018

!!! info "Driving Restrictions"
    Non-ACC vehicles have a minimum enable speed of 24 mph and a minimum steer speed of 3.0 m/s. Steering assistance is not available below these thresholds.

!!! warning "Testing Status"
    Some Non-ACC platforms are in dashcam mode (untested). These vehicles run sunnypilot in a monitoring-only mode until community testing validates full steering support.

---

## Steering Torque Models

sunnypilot uses vehicle-specific steering torque models to optimize lateral control for GM vehicles:

| Vehicle | Model Type | Description |
|---------|-----------|-------------|
| Bolt EUV | Neural network feedforward | A 4-layer neural network that provides precise steering response |
| Bolt EUV, Acadia, Silverado | Sigmoid-linear (SigLin) | A non-linear torque curve that reduces steering noise on straight roads while maintaining responsiveness in turns |
| Other GM vehicles | Linear | Standard linear torque mapping |

These models are applied automatically based on your vehicle — no configuration is needed.
