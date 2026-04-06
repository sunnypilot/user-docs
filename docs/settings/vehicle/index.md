---
title: Vehicle Settings
---

# Vehicle Settings

View and manage vehicle-specific settings. The content of this panel changes based on your connected or manually selected vehicle.

**Location**: `Settings -> Vehicle`

!!! info "Toggle & Device Availability"
    Supported on all devices. comma four users must use sunnylink to change this setting.

---

## Vehicle Selection

At the top of the panel, the currently detected or selected vehicle is displayed. The vehicle name is color-coded:

| Color | Meaning |
|-------|---------|
| **Green** | Vehicle was automatically fingerprinted (detected) |
| **Blue** | Vehicle was manually selected |
| **Yellow** | Vehicle could not be fingerprinted |

- **SELECT** button: Opens a vehicle selection dialog where you can manually choose your vehicle make and model.
- **REMOVE** button: Clears the manual selection and returns to automatic fingerprinting.

A legend below the vehicle name explains the color codes.

---

## Brand-Specific Settings

After a vehicle is detected or selected, brand-specific settings appear below the vehicle selector. Only brands with configurable settings show additional items:

- [Chrysler / Dodge / Jeep / RAM](chrysler.md) - MADS via LKAS, ICBM, Steer to Zero
- [Ford](ford.md) - MADS support
- [GM / Chevrolet](gm.md) - Non-ACC vehicle support, custom torque models
- [Honda / Acura](honda.md) - Gas Interceptor, ICBM, MADS, Nidec hybrid support
- [Hyundai / Kia / Genesis](hyundai.md) - MADS, ICBM, Custom Longitudinal Tuning, ESCC
- [Mazda](mazda.md) - ICBM support
- [Nissan](nissan.md) - Leaf-specific behavior
- [Rivian](rivian.md) - Longitudinal harness upgrade, MADS limitations
- [Subaru](subaru.md) - Stop and Go, Stop and Go for Manual Parking Brake
- [Tesla](tesla.md) - Cooperative Steering
- [Toyota / Lexus](toyota.md) - Enforce Factory Longitudinal Control, Stop and Go Hack, ZSS, Gas Interceptor

The following brands are supported for vehicle selection but have no brand-specific settings page: Volkswagen, PSA.
