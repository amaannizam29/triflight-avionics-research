# TriFlight Pin Mapping Template

| FC Port | Assigned Device | Signal Type | Voltage | Notes |
|---|---|---|---|---|
| SERVO1 | Left aileron | PWM | 5V servo rail | Check deflection direction |
| SERVO2 | Right aileron | PWM | 5V servo rail | Opposite to SERVO1 for roll |
| SERVO3 | Left V-tail | PWM | 5V servo rail | V-tail mix: pitch + yaw |
| SERVO4 | Right V-tail | PWM | 5V servo rail | V-tail mix: pitch + yaw |
| SERVO5 | ESC throttle | PWM/DShot | Signal + GND only | Remove prop during setup |
| UART1 | GPS | Serial TX/RX | 5V | TX/RX crossed between devices |
| I2C | Compass / airspeed | I2C SDA/SCL | 3.3V or 5V | Check device voltage tolerance |
| UART2 | Telemetry radio | MAVLink serial | 5V | Baud rate must match radio |
| RCIN | ELRS receiver | CRSF/SBUS | 5V | Bind and range test before flight |
| ADC/PM | Power module | Analog | VBAT scaled | Calibrate in Mission Planner |
