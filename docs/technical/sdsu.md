---
title: Smart DSU (SDSU)
---

# Smart DSU (SDSU)

## Overview

The Smart DSU (SDSU) is a hardware module for Toyota and Lexus vehicles, similar in concept to Hyundai/Kia/Genesis's [ESCC](escc.md). It is installed at the radar (DSU — Driving Support Unit) and enables sunnypilot to take over longitudinal control while retaining factory FCW (Forward Collision Warning) and AEB (Automatic Emergency Braking) functionality.

Not all Toyota/Lexus vehicles need an SDSU — only those where sunnypilot cannot intercept longitudinal messages without disabling factory safety systems.

## Why SDSU Exists

Some Toyota and Lexus vehicles can only enable sunnypilot longitudinal control by disabling the DSU in software. While this works, it disables factory FCW and AEB. The SDSU solves this by intercepting the messages at the radar so that sunnypilot's commands do not collide with the DSU's own messages. This allows longitudinal control — including stop-and-go (slowing to 0 and resuming) — without sacrificing factory safety.

## How It Works

The SDSU module sits at the DSU and intercepts the messages that sunnypilot needs to send to the vehicle, preventing collisions between the DSU's messages and sunnypilot's commands. This gives sunnypilot full longitudinal authority while the DSU continues to handle FCW and AEB independently.

## Safety

The SDSU preserves all factory safety systems. FCW and AEB continue to function normally — sunnypilot does not interfere with these safety-critical signals.

## Requirements

!!! info "Requirements"
    - A Toyota or Lexus vehicle where longitudinal control requires DSU interception
    - An SDSU module installed at the DSU

!!! tip "Detection"
    sunnypilot automatically detects the SDSU when present. No additional user configuration is needed.

## Related

- [ESCC](escc.md) — Equivalent hardware module for Hyundai/Kia/Genesis
- [Gas Interceptor (comma Pedal)](gas-interceptor.md) — Alternative hardware for longitudinal control
- [Toyota / Lexus Settings](../settings/vehicle/toyota.md)
- [Alpha Longitudinal](../features/cruise/alpha-longitudinal.md)
