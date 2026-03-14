---
title: Honda / Acura Settings
---

# Honda / Acura Vehicle Settings

Information about sunnypilot behavior on Honda and Acura vehicles. These notes apply when a Honda or Acura vehicle is connected or selected.

**Location**: `Settings -> Vehicle`

---

## Gas Interceptor (comma Pedal)

Honda and Acura vehicles that use a Gas Interceptor (commonly known as comma Pedal) gain longitudinal control through sunnypilot. The accelerator command scales with vehicle speed — lower output at low speeds, increasing to full scale above approximately 10 m/s. Wind brake compensation is applied at higher speeds.

!!! info "Platform Restriction"
    The Gas Interceptor is only supported on non-Bosch Honda/Acura platforms. Bosch-equipped vehicles skip Gas Interceptor detection entirely.

See the [Gas Interceptor (comma Pedal)](../../how-to/gas-interceptor.md) guide for details.

---

## ICBM Support

Honda and Acura vehicles without native longitudinal control can use [Intelligent Cruise Button Management (ICBM)](../../features/cruise/icbm.md). ICBM simulates cruise button presses (resume/accel and decel/set) at 50 ms intervals to manage set speed through the vehicle's stock cruise control system.

!!! info "Availability"
    Available on Bosch non-CAN FD platforms. CAN FD Honda models may have ICBM on development branches only.

---

## MADS Behavior

When [MADS](../../features/steering/mads.md) is enabled on Honda vehicles, the onroad display shows dashed lane lines when lateral control is available but not actively engaged. This provides a visual indicator that steering assistance is standing by.

On Bosch radarless models, the lane visibility behavior follows the stock HUD value.

---

## Nidec Hybrid Support

Honda hybrid vehicles using the Nidec ADAS system have specialized brake signal handling. sunnypilot reads additional brake fault and AEB status signals, and supports an alternate brake-hold detection path for hybrid variants. In practice, this primarily applies to the Honda Clarity.

---

## Modified EPS Support

Some Honda vehicles with aftermarket or modified Electric Power Steering (EPS) systems are supported through a dedicated flag. This adjusts the steering interface to work with non-stock EPS hardware. Modified EPS is detected automatically from the EPS firmware version during fingerprinting — no user configuration is needed.
