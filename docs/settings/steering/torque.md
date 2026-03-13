---
title: Torque Settings
---

# Torque Settings

Advanced tuning parameters for torque-based lateral (steering) control. These settings give you fine-grained control over how the steering motor responds.

**Location**: `Settings -> Steering -> Customize Torque Params`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

!!! info "Prerequisite"
    **Enforce Torque Lateral Control** must be enabled in [Steering Settings](index.md) to access this sub-panel. Not available on vehicles with angle-based steering.

!!! warning "Offroad Only"
    All torque settings can only be changed while the vehicle is offroad (parked with ignition off).

---

## Torque Control Tune Version

A button that opens a version selector. Choose which version of the torque control tuning algorithm to use. Newer versions may offer improved performance but can behave differently than what you are accustomed to.

---

## Self-Tune

Enables real-time self-tuning of torque parameters based on your driving behavior. The system continuously adjusts lateral acceleration factor and friction values for optimal steering feel.

---

## Less Restrict Settings for Self-Tune (Beta)

Uses a more relaxed self-tuning profile. The torque controller is more forgiving when learning values, which may provide a smoother but less responsive steering feel.

!!! note "Availability"
    This toggle only appears when **Self-Tune** is enabled.

---

## Enable Custom Tuning

Enables manual override of torque control parameters. When enabled, you can set specific values for lateral acceleration and friction instead of relying on self-tuning. The values you set here override the offline values from the vehicle's tuning data files.

---

## Manual Real-Time Tuning

Forces the torque controller to use your fixed custom values instead of the learned values from Self-Tune. Enabling this overrides Self-Tune values in real time.

!!! note "Availability"
    This toggle only appears when **Enable Custom Tuning** is enabled.

---

## Lateral Acceleration Factor

A slider that controls the lateral acceleration gain. Use the **-** and **+** buttons to adjust. The value displays as a decimal (e.g., 1.50 means 1.50x lateral acceleration factor).

Higher values produce more aggressive steering response. Lower values produce softer response.

!!! note "Availability"
    This slider only appears when **Enable Custom Tuning** is enabled.

---

## Friction

A slider that controls the friction compensation factor. Use the **-** and **+** buttons to adjust. The value displays as a decimal (e.g., 0.75).

Adjusts how much the system compensates for steering friction in your vehicle.

!!! note "Availability"
    This slider only appears when **Enable Custom Tuning** is enabled.

---

## Related Features

- [Torque Control](../../features/steering/torque-control.md)
