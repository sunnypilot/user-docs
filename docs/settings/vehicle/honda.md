---
title: Honda / Acura Settings
---

# Honda / Acura Vehicle Settings

Information about sunnypilot behavior on Honda and Acura vehicles. These notes apply when a Honda or Acura vehicle is connected or selected.

**Location**: `Settings -> Vehicle`

---

## Gas Interceptor (comma Pedal)

Honda and Acura vehicles that use a Gas Interceptor (commonly known as comma Pedal) gain longitudinal control through sunnypilot. The gas command scales with vehicle speed — lower gas output at low speeds, increasing to full scale above approximately 10 m/s. Wind brake compensation is applied at higher speeds.

See the [Gas Interceptor (comma Pedal)](../../how-to/gas-interceptor.md) guide for details.

---

## ICBM Support

Honda and Acura vehicles without native longitudinal control can use [Intelligent Cruise Button Management (ICBM)](../../features/cruise/icbm.md). ICBM simulates cruise button presses (resume/accel and decel/set) at 50 ms intervals to manage set speed through the vehicle's stock cruise control system.

---

## MADS Behavior

When [MADS](../../features/steering/mads.md) is enabled on Honda vehicles, the onroad display shows dashed lane lines when lateral control is available but not actively engaged. This provides a visual indicator that steering assistance is standing by.

On Bosch radarless models, the lane visibility behavior follows the stock HUD value.

---

## Nidec Hybrid Support

Honda hybrid vehicles using the Nidec ADAS system have specialized brake signal handling. sunnypilot reads additional brake fault and AEB status signals, and supports an alternate brake-hold detection path for hybrid variants.

---

## Modified EPS Support

Some Honda vehicles with aftermarket or modified Electric Power Steering (EPS) systems are supported through a dedicated flag. This adjusts the steering interface to work with non-stock EPS hardware.
