# TriFlight Bench-Test Protocol

All motor/ESC tests must be performed with the propeller removed.

| Test | Procedure | Pass Criteria | Status |
|---|---|---|---|
| Continuity | Confirm common ground and no VBAT-to-GND short | No short; common ground confirmed | Pending hardware |
| Polarity | Check battery connector, ESC, power module, 5V rail | Correct polarity | Pending hardware |
| 5V Rail Idle | Power system without servo movement | 4.9V–5.2V stable | Pending hardware |
| Servo Load | Move all surfaces for 60 seconds | No brownout | Pending hardware |
| ESC Signal | Arm and increase throttle slowly, prop removed | Motor responds smoothly | Pending hardware |
| GPS Lock | Outdoor GPS fix test | Stable 3D fix, HDOP < 2.0 | Pending hardware |
| Failsafe | Simulate RC loss, prop removed | Expected failsafe mode triggers | Pending hardware |
| Telemetry Link | Run Mission Planner / Python logger | Heartbeat received, CSV populated | Pending hardware |
