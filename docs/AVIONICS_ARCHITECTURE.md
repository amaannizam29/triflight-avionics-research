# Avionics Architecture — Talon QuadPlane Conversion

System-level avionics definition for the VTOL conversion. Component choices are a
standard Talon-class QuadPlane stack; values marked *(verify)* should be checked
against the actual build before use.

## System block diagram (summary)

```
Battery (6S) → Power Module → Flight Controller → ESCs (x5) → Motors (x5)
                                   ↑
        GPS · Compass · IMU · Barometer · Airspeed · Telemetry · RC receiver
```

Power flows battery → power module → flight controller and ESCs → motors.
Sensors and radio links feed data into the flight controller. The flight
controller closes the loop: it reads sensors, runs the EKF and control laws, and
commands the ESCs.

## Power budget

Worst case is hover (all four lift motors near full thrust). Cruise is far lower
because lift motors are off and only the pusher runs.

| Item | Qty | Draw each | Total | Notes |
|---|---|---|---|---|
| Lift motors (hover) | 4 | ~10 A | ~40 A | peak load, transition/hover *(verify)* |
| Pusher motor (cruise) | 1 | ~9 A | ~9 A | forward flight |
| Flight controller | 1 | ~0.3 A | 0.3 A | via BEC |
| GPS + compass | 1 | ~0.1 A | 0.1 A | |
| Telemetry radio | 1 | ~0.2 A | 0.2 A | peak on transmit |
| RC receiver | 1 | ~0.1 A | 0.1 A | |
| Airspeed sensor | 1 | ~0.02 A | 0.02 A | |
| **Peak (hover)** | | | **~41 A** | sizes ESC + wiring |
| **Cruise** | | | **~10 A** | sets endurance |

Pack: 6S, ~8000 mAh *(verify)*. Main leads sized for the ~41 A hover peak (12 AWG
or heavier). Endurance is set by cruise draw, not hover, since hover is brief.

## Sensor table

| Sensor | Measures | Interface | Feeds | Fault mode (detected) |
|---|---|---|---|---|
| GPS | Position, satellites, HDOP | UART | EKF position | GPS fault |
| Compass | Heading, magnetic field | I2C | EKF yaw | Compass fault |
| IMU | Angular rate, acceleration | SPI/I2C | EKF attitude | (vibration → motor) |
| Barometer | Altitude (pressure) | I2C | EKF altitude | — |
| Airspeed (pitot) | Forward airspeed | I2C | Transition logic | — |
| Power module | Voltage, current | Analog/I2C | Battery monitor | Battery fault |
| ESC telemetry | Motor RPM/current | (optional) | Motor health | Motor fault |

The four fault modes in the failure-detection system map directly onto these
sensors: GPS, compass, battery (power module), and motor (ESC/IMU signatures).

## Communication table

| Link | From → To | Protocol | Direction | Purpose |
|---|---|---|---|---|
| GPS link | GPS → FC | UART (MAVLink/UBX) | in | Position data |
| Compass link | Compass → FC | I2C | in | Heading |
| IMU/baro link | Sensors → FC | SPI / I2C | in | Attitude, altitude |
| Airspeed link | Pitot → FC | I2C | in | Airspeed |
| Telemetry | FC ↔ Ground | MAVLink over radio | bidirectional | Telemetry out, commands in |
| RC control | TX → RX → FC | ELRS/SBUS *(verify)* | in | Pilot control |
| Motor command | FC → ESC | PWM/DShot *(verify)* | out | Throttle per motor |

The telemetry link is the one the failure-detection system rides on: it reads
MAVLink telemetry coming down, and command-out (LAND/RTL) goes back up the same
link.

## Notes

- This is the integration-level architecture, not a claim of airframe design. The
  Talon platform is existing; this defines how the avionics stack is wired and
  how data flows.
- Verify every *(verify)* value and the exact part numbers against the real build
  before relying on the power budget.
