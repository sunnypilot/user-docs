---
title: Alpha Longitudinal
---

# Alpha Longitudinal

!!! tip "Does this apply to my car?"
    Check the **ACC** column on the [sunnypilot supported vehicles list](https://github.com/sunnypilot/sunnypilot/blob/master/docs/CARS.md).

    - **"openpilot"** — Your car has full native longitudinal control. It is always active, no toggle is needed, and **Alpha Longitudinal does not apply to you**.
    - **"openpilot available"** — Your car can optionally use Alpha Longitudinal. Read on.
    - **"stock"** — Your car does not support sunnypilot longitudinal. However, if you have installed aftermarket hardware like a [Smart DSU](../../settings/vehicle/toyota.md#smart-dsu) or [Gas Interceptor](../../how-to/gas-interceptor.md) (Toyota/Lexus) or a [Longitudinal Harness Upgrade](../../settings/vehicle/rivian.md#longitudinal-harness-upgrade) (Rivian), these mods enable Alpha Longitudinal on your car even though it would otherwise have no longitudinal support. See [Hardware Mods That Require Alpha Longitudinal](#hardware-mods-that-require-alpha-longitudinal) below.

## What It Does

Alpha Longitudinal lets sunnypilot optionally take over acceleration and braking on vehicles where longitudinal control is *possible* but not yet considered release-quality. These cars show **"openpilot available"** in the ACC column — meaning the capability exists, but it comes with trade-offs that cars with native longitudinal support ("openpilot" in the ACC column) do not have.

Some vehicles that would otherwise show "stock" in the ACC column can also gain Alpha Longitudinal through aftermarket hardware modifications. In these cases, the hardware creates the capability and Alpha Longitudinal is the gate that activates it.

### Why "Alpha"?

For cars with native longitudinal support, comma and sunnypilot have fully validated the integration — factory safety systems are preserved, tuning is refined, and the experience is release-ready. Alpha Longitudinal vehicles have not yet reached that bar. The main reasons are:

- **Factory safety systems may be affected.** On most Alpha Longitudinal vehicles, enabling sunnypilot longitudinal control disables the factory ACC module, and because many OEMs bundle ACC, FCW, and AEB in the same module, factory FCW/AEB may also be disabled. However, **some vehicles do retain factory FCW/AEB** even with Alpha Longitudinal enabled — the behavior varies by vehicle and platform.
- **Tuning is less refined.** Acceleration, braking, and stop-and-go behavior may feel rougher compared to natively supported cars.
- **Radar parsing and driving models are improving.** As radar integration improves and driving models become more capable, the experience on these vehicles will get better over time. Alpha Longitudinal exists as a bridge to let users opt in today while development continues.

If your vehicle's dashboard shows an amber FCW/AEB warning icon after enabling Alpha Longitudinal, this typically indicates the factory system has been displaced — this is expected on vehicles where the OEM bundles these systems together. On vehicles that retain factory safety systems, no such indicator will appear.

!!! danger "Understand the trade-offs"
    On vehicles where factory AEB is disabled, the vehicle will not automatically apply emergency braking in imminent collision scenarios. Drive with extra caution and maintain safe following distances at all times. **Know your vehicle** — check community resources to understand whether your specific car retains factory FCW/AEB with Alpha Longitudinal enabled.

## Which Cars Can Use It

Only cars that show **"openpilot available"** in the **ACC** column are eligible. If a car does not have that designation:

- The toggle will not appear in the UI
- sunnypilot will always use stock longitudinal control (stock ACC)

The specific conditions that make `alphaLongitudinalAvailable` true vary by brand:

| Brand | Condition |
|-------|-----------|
| **Tesla** | All vehicles |
| **Honda / Acura** | Bosch non-CAN FD platforms |
| **Hyundai / Kia / Genesis** | Most models not in the unsupported longitudinal list; disabled for Non-SCC vehicles |
| **GM / Chevrolet** | Camera ACC vehicles (not SDGM, not ALT_ACC); disabled for Non-ACC vehicles |
| **Toyota / Lexus** | Radar ACC vehicles, or when a [Smart DSU](../../settings/vehicle/toyota.md#smart-dsu) or [Gas Interceptor](../../how-to/gas-interceptor.md) is detected |
| **Ford** | Radarless vehicles only |
| **Volkswagen** | Gateway network location vehicles |
| **Subaru** | Global Gen 1 non-hybrid, non-LKAS angle vehicles |
| **Rivian** | Only with [Longitudinal Harness Upgrade](../../settings/vehicle/rivian.md#longitudinal-harness-upgrade) detected |

Brands not listed (Nissan, Mazda, Chrysler, PSA) do not have Alpha Longitudinal support.

## How It Works

### Two-Stage Enablement

Alpha Longitudinal has two gates that must both be satisfied:

1. **`alphaLongitudinalAvailable`** — Set automatically during vehicle fingerprinting (or loaded from cached fingerprint data via `CarParamsPersistence`) based on the vehicle model and detected hardware. This determines whether the toggle appears in the UI.

2. **`AlphaLongitudinalEnabled`** — The user's toggle in **Settings -> Developer -> sunnypilot Longitudinal Control (Alpha)**. When the user enables this, sunnypilot sets `openpilotLongitudinalControl` to true in the car interface, which activates direct acceleration and braking control and sets `pcmCruise` to false.

!!! note "Vehicle Must Be Recognized First"
    The vehicle must be started and recognized by sunnypilot **at least once** before the toggle becomes available. The toggle will not display until sunnypilot has fully identified the vehicle and cached the fingerprint.

### What Happens When Enabled

When the toggle is enabled:

- sunnypilot takes full control of longitudinal behavior (acceleration and braking)
- The vehicle's stock ACC system is bypassed (`pcmCruise=False`)
- On most vehicles, a FCW/AEB dashboard indicator may illuminate, indicating that the factory system is affected — some vehicles retain factory FCW/AEB, others do not
- [Experimental Mode](../../settings/toggles/index.md) becomes available

When the toggle is off or unavailable, the vehicle is always using stock longitudinal control.

## Hardware Mods That Require Alpha Longitudinal

Some cars do not natively support sunnypilot longitudinal control, but aftermarket hardware can add that capability. When sunnypilot detects these hardware mods during fingerprinting, it sets `alphaLongitudinalAvailable` to true — but the user **must** then enable Alpha Longitudinal in Developer settings for the hardware to actually function. Installing the hardware alone is not enough.

| Hardware Mod | Brand | What It Does | Details |
|---|---|---|---|
| **Smart DSU** | Toyota/Lexus (TSS 1.0) | Overrides the factory DSU to give sunnypilot longitudinal control and stop-and-go | [Smart DSU details](../../settings/vehicle/toyota.md#smart-dsu) |
| **Gas Interceptor (comma Pedal)** | Toyota/Lexus | Intercepts the accelerator pedal signal to give sunnypilot longitudinal control and stop-and-go. Not compatible with SecOC vehicles. | [Gas Interceptor details](../../how-to/gas-interceptor.md) |
| **Longitudinal Harness Upgrade** | Rivian | Custom harness that enables radar, BSM, and longitudinal control | [Harness Upgrade details](../../settings/vehicle/rivian.md#longitudinal-harness-upgrade) |

!!! note "These cars may share a brand with natively supported models"
    For example, many Toyota TSS2 vehicles already have native longitudinal ("openpilot" in ACC) and do not need Alpha Longitudinal at all. But a Toyota TSS 1.0 vehicle with a Smart DSU installed *does* need Alpha Longitudinal — the mod creates the capability, and the toggle activates it. The requirement depends on your specific vehicle and hardware configuration, not just the brand.

There are also **unofficial third-party hardware solutions** that allow users to retain factory FCW/AEB while using sunnypilot Longitudinal Control (Alpha). Some are officially supported in sunnypilot.

## Experimental Mode Requirement

To use **Experimental Mode**, longitudinal control must be active. For vehicles where Alpha Longitudinal is the only path to longitudinal control, this means the Alpha Longitudinal toggle must be enabled. If the toggle is off, unavailable, or the car is unsupported, Experimental Mode is not available.

## sunnypilot vs. openpilot

!!! info "Topic Compatibility"
    Most sections of this page also apply to [commaai's openpilot](https://github.com/commaai/openpilot). The differences are noted below.

| | sunnypilot | openpilot |
|---|---|---|
| **Branch availability** | All branches (release, staging, dev) | Non-release branches only (devel, nightly-dev) |
| **Aftermarket hardware** | Smart DSU, Gas Interceptor, and other mods are recognized and supported | Does not support or recognize unofficial hardware |

In openpilot, release branches **never** offer the Alpha Longitudinal toggle. Installing any release branch of openpilot will always result in stock ACC behavior, regardless of vehicle support. Any perceived change in braking or following distance on a release branch is placebo.

## How to Enable

1. Ensure your vehicle is recognized by sunnypilot (start the car at least once)
2. Go to **Settings -> Developer**
3. Enable **sunnypilot Longitudinal Control (Alpha)**

!!! note
    This toggle only appears for vehicles where `alphaLongitudinalAvailable` is true. On some newer software, it may appear as **Alpha Longitudinal**.

!!! warning "Mutually Exclusive with ICBM"
    Alpha Longitudinal and [ICBM](icbm.md) cannot be active at the same time. Enabling Alpha Longitudinal disables ICBM, and vice versa. Alpha Longitudinal provides direct longitudinal control, while ICBM works through the stock cruise control system — these two approaches are fundamentally incompatible.

## Summary

- **Cars with "openpilot" in the ACC column already have native longitudinal — Alpha Longitudinal does not apply to them**
- Only cars marked **"openpilot available"** under ACC can use Alpha Longitudinal
- Alpha Longitudinal is an opt-in bridge for vehicles where longitudinal control works but is not yet release-quality
- Most vehicles lose factory FCW/AEB, but some retain it — check community resources for your specific car
- The experience will improve over time as radar parsing and driving models advance
- sunnypilot must recognize the vehicle **at least once** before the toggle appears
- **openpilot only:** Release branches never offer this toggle
- Toggle off or missing = stock ACC
- Experimental Mode requires longitudinal control to be active
- Some aftermarket hardware (Smart DSU, Gas Interceptor, Rivian harness) requires Alpha Longitudinal to be enabled to function

## Settings Reference

See [Cruise Control Settings](../../settings/cruise/index.md) for configuration details.
