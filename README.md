# TriFlight Initiative — UAV Avionics Research

TriFlight is a pre-experimental UAV avionics and systems-integration research project focused on a fixed-wing UAV platform.

The project remained at research/software/planning stage due to lack of hardware funding. No flight, bench, or hardware validation results are claimed.

## Completed Work

- UAV avionics architecture design
- Power and signal mapping
- ArduPilot / INAV / PX4 firmware comparison
- MAVLink telemetry logger implementation
- Bench-test and flight-test validation plan
- Evidence checklist for future hardware implementation

## Repository Structure

```text
triflight-avionics-research/
├── README.md
├── LICENSE.md
├── requirements.txt
├── src/
│   └── triflight_mavlink_logger.py
├── docs/
│   ├── evidence_checklist.md
│   ├── pin_mapping_template.md
│   └── bench_test_protocol.md
└── sample_data/
    └── sample_log_format.csv
```

## MAVLink Logger

The logger is a read-only Python script. It connects to a MAVLink stream from ArduPilot SITL, a real flight controller, or a telemetry radio and records selected telemetry fields into a CSV file.

It does not send control commands.

## Install

```bash
pip install -r requirements.txt
```

## Example Usage

Serial connection:

```bash
python src/triflight_mavlink_logger.py --conn COM7 --baud 57600 --out triflight_log.csv
```

ArduPilot SITL / UDP:

```bash
python src/triflight_mavlink_logger.py --conn udp:127.0.0.1:14550 --out triflight_sitl_log.csv
```

## Status

Research and software documentation complete. Hardware testing pending.

## Research Report

📄 Full report:  
[TriFlight Avionics Research Report](docs/TriFlight_Research_Paper_V3.pdf)

Includes system architecture, avionics design, MAVLink telemetry, and validation methodology.  
No experimental results are included — hardware testing pending.
