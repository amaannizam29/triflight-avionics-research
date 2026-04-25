#!/usr/bin/env python3
"""
TriFlight MAVLink Telemetry Logger

Read-only telemetry logger for fixed-wing UAV research.

It listens to MAVLink messages and writes selected fields into CSV format.
It does not send commands to the flight controller.

Example:
    python triflight_mavlink_logger.py --conn COM7 --baud 57600 --out triflight_log.csv
    python triflight_mavlink_logger.py --conn udp:127.0.0.1:14550 --out triflight_sitl_log.csv
"""

import argparse
import csv
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pymavlink import mavutil


FIELDS = [
    "utc_time",
    "mode",
    "msg_type",
    "lat_deg",
    "lon_deg",
    "relative_alt_m",
    "groundspeed_mps",
    "airspeed_mps",
    "roll_deg",
    "pitch_deg",
    "yaw_deg",
    "battery_voltage_v",
    "battery_current_a",
    "battery_remaining_pct",
]


def deg_from_e7(value: Optional[int]) -> Optional[float]:
    return None if value is None else value / 1e7


def m_from_mm(value: Optional[int]) -> Optional[float]:
    return None if value is None else value / 1000.0


def deg_from_rad(value: Optional[float]) -> Optional[float]:
    return None if value is None else value * 57.2957795


def create_initial_state() -> Dict[str, Any]:
    return {field: None for field in FIELDS}


def update_state_from_message(state: Dict[str, Any], master: Any, msg: Any) -> bool:
    msg_type = msg.get_type()

    state["utc_time"] = datetime.now(timezone.utc).isoformat()
    state["mode"] = getattr(master, "flightmode", None)
    state["msg_type"] = msg_type

    if msg_type == "GLOBAL_POSITION_INT":
        state["lat_deg"] = deg_from_e7(getattr(msg, "lat", None))
        state["lon_deg"] = deg_from_e7(getattr(msg, "lon", None))
        state["relative_alt_m"] = m_from_mm(getattr(msg, "relative_alt", None))

        vx = getattr(msg, "vx", None)
        vy = getattr(msg, "vy", None)
        if vx is not None and vy is not None:
            state["groundspeed_mps"] = ((vx ** 2 + vy ** 2) ** 0.5) / 100.0
        return True

    if msg_type == "VFR_HUD":
        state["airspeed_mps"] = getattr(msg, "airspeed", None)
        state["groundspeed_mps"] = getattr(msg, "groundspeed", state.get("groundspeed_mps"))
        return True

    if msg_type == "ATTITUDE":
        state["roll_deg"] = deg_from_rad(getattr(msg, "roll", None))
        state["pitch_deg"] = deg_from_rad(getattr(msg, "pitch", None))
        state["yaw_deg"] = deg_from_rad(getattr(msg, "yaw", None))
        return True

    if msg_type == "BATTERY_STATUS":
        voltages = getattr(msg, "voltages", [])
        valid_voltages = [v for v in voltages if v != 65535]

        if valid_voltages:
            state["battery_voltage_v"] = sum(valid_voltages) / 1000.0

        current_battery = getattr(msg, "current_battery", -1)
        if current_battery != -1:
            state["battery_current_a"] = current_battery / 100.0

        battery_remaining = getattr(msg, "battery_remaining", -1)
        if battery_remaining != -1:
            state["battery_remaining_pct"] = battery_remaining

        return True

    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="TriFlight MAVLink CSV telemetry logger")
    parser.add_argument("--conn", required=True, help="Connection string, e.g. COM7 or udp:127.0.0.1:14550")
    parser.add_argument("--baud", type=int, default=57600, help="Serial baud rate; ignored for UDP")
    parser.add_argument("--out", default="triflight_telemetry.csv", help="Output CSV filename")
    parser.add_argument("--rate", type=float, default=0.5, help="Minimum seconds between CSV writes")
    parser.add_argument("--heartbeat-timeout", type=int, default=30, help="Heartbeat timeout in seconds")
    args = parser.parse_args()

    print(f"Connecting to MAVLink source: {args.conn}")
    master = mavutil.mavlink_connection(args.conn, baud=args.baud)

    print("Waiting for heartbeat...")
    master.wait_heartbeat(timeout=args.heartbeat_timeout)
    print(f"Connected to system={master.target_system}, component={master.target_component}")

    state = create_initial_state()
    last_write = 0.0

    with open(args.out, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDS)
        writer.writeheader()

        print(f"Logging to {args.out}. Press Ctrl+C to stop.")
        try:
            while True:
                msg = master.recv_match(blocking=True, timeout=1)
                if msg is None:
                    continue

                useful = update_state_from_message(state, master, msg)
                now = time.time()

                if useful and (now - last_write >= args.rate):
                    writer.writerow(state)
                    csv_file.flush()
                    last_write = now

        except KeyboardInterrupt:
            print("\nLogging stopped by user.")


if __name__ == "__main__":
    main()
