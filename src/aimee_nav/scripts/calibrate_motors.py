#!/usr/bin/env python3
"""
Motor calibration script for Wave Rover.

Uses IMU yaw feedback (T=1001 over serial) to verify rotation,
and lidar front distance to verify translation.

Run this with the robot on the floor in an open area (at least 1m clear ahead).
"""

import json
import math
import time
import urllib.request
import urllib.parse

import serial

from aimee_nav.ld19_driver import LD19Driver


ROVER_HTTP_IP = "192.168.1.56"
ROVER_SERIAL = "/dev/ttyUSB0"
LIDAR_SERIAL = "/dev/ttyUSB1"


def send_motor_cmd(L: float, R: float) -> None:
    """Send T=1 wheel speed command via HTTP."""
    cmd = {"T": 1, "L": round(L, 3), "R": round(R, 3)}
    j = json.dumps(cmd, separators=(",", ":"))
    enc = urllib.parse.quote(j, safe="")
    url = f"http://{ROVER_HTTP_IP}/js?json={enc}"
    try:
        req = urllib.request.Request(url, headers={"Connection": "close"})
        with urllib.request.urlopen(req, timeout=2) as resp:
            resp.read()
    except Exception:
        pass


def enable_imu_feedback(ser: serial.Serial) -> None:
    """Send T=131 to enable continuous T=1001 feedback."""
    payload = json.dumps({"T": 131, "cmd": 1}, separators=(",", ":")) + "\n"
    ser.write(payload.encode("utf-8"))
    ser.flush()
    time.sleep(0.2)


def read_imu_yaw(ser: serial.Serial, timeout: float = 1.0) -> float:
    """Read T=1001 packets and return yaw in degrees."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            line = ser.readline().decode("utf-8").strip()
            if not line:
                continue
            msg = json.loads(line)
            if msg.get("T") == 1001:
                return float(msg.get("y", 0.0))
        except Exception:
            continue
    return float("nan")


def yaw_diff(a: float, b: float) -> float:
    """Smallest signed angle difference in degrees."""
    d = ((b - a + 180) % 360) - 180
    return d


def get_lidar_front_distance(driver: LD19Driver, timeout: float = 2.0) -> float:
    """Get the median front distance (0° ± 5°) from lidar."""
    deadline = time.time() + timeout
    distances = []
    while time.time() < deadline:
        scan = driver.get_scan(block=True, timeout=0.5)
        if scan is None:
            continue
        for p in scan.points:
            if abs(p.angle_deg) <= 5.0 or abs(p.angle_deg - 360.0) <= 5.0:
                if 0.05 < p.distance_m < 12.0:
                    distances.append(p.distance_m)
        if len(distances) >= 3:
            distances.sort()
            return distances[len(distances) // 2]
    return float("nan")


def calibrate_rotation(ser: serial.Serial) -> dict:
    """Find minimum power needed for reliable in-place rotation."""
    print("\n--- CALIBRATING ROTATION ---")
    print("Robot will spin left in short bursts. Please keep clear.")
    time.sleep(2)

    results = {}
    for power in [0.3, 0.5, 0.7, 0.8, 1.0]:
        print(f"\nTrying spin power = {power}")
        # Take baseline yaw
        yaw_before = read_imu_yaw(ser)
        if math.isnan(yaw_before):
            print("  Failed to read IMU yaw")
            continue

        # Spin left for 1 second
        send_motor_cmd(-power, power)
        time.sleep(1.0)
        send_motor_cmd(0.0, 0.0)
        time.sleep(0.5)

        yaw_after = read_imu_yaw(ser)
        if math.isnan(yaw_after):
            print("  Failed to read IMU yaw after spin")
            continue

        delta = abs(yaw_diff(yaw_before, yaw_after))
        print(f"  Yaw change: {delta:.1f}°")

        if delta >= 15.0:
            results["min_spin_power"] = power
            results["spin_yaw_rate_dps"] = delta
            print(f"  ✓ Reliable spin at power {power}")
            break
        elif delta >= 5.0:
            print(f"  ~ Weak spin at power {power}")
            if "min_spin_power" not in results:
                results["min_spin_power"] = power
                results["spin_yaw_rate_dps"] = delta
        else:
            print(f"  ✗ No significant rotation")

    if "min_spin_power" not in results:
        print("WARNING: Could not achieve reliable rotation at max power")
        results["min_spin_power"] = 1.0
        results["spin_yaw_rate_dps"] = 0.0

    return results


def calibrate_forward(driver: LD19Driver) -> dict:
    """Find minimum power needed for reliable forward movement."""
    print("\n--- CALIBRATING FORWARD ---")
    print("Robot will drive forward in short bursts. Need ~1m clear ahead.")
    time.sleep(2)

    results = {}
    for power in [0.1, 0.2, 0.3, 0.4, 0.5]:
        print(f"\nTrying forward power = {power}")
        dist_before = get_lidar_front_distance(driver)
        if math.isnan(dist_before):
            print("  Failed to read lidar")
            continue
        print(f"  Front distance before: {dist_before:.2f}m")

        # Drive forward for 1 second
        send_motor_cmd(power, power)
        time.sleep(1.0)
        send_motor_cmd(0.0, 0.0)
        time.sleep(0.5)

        dist_after = get_lidar_front_distance(driver)
        if math.isnan(dist_after):
            print("  Failed to read lidar after move")
            continue
        print(f"  Front distance after:  {dist_after:.2f}m")

        delta = dist_before - dist_after
        print(f"  Distance closed: {delta:.2f}m")

        if delta >= 0.05:
            results["min_fwd_power"] = power
            results["fwd_speed_mps"] = delta
            print(f"  ✓ Reliable forward at power {power}")
            break
        elif delta >= 0.02:
            print(f"  ~ Weak forward at power {power}")
            if "min_fwd_power" not in results:
                results["min_fwd_power"] = power
                results["fwd_speed_mps"] = delta
        else:
            print(f"  ✗ No significant forward movement")

    if "min_fwd_power" not in results:
        print("WARNING: Could not achieve reliable forward at max power")
        results["min_fwd_power"] = 0.5
        results["fwd_speed_mps"] = 0.0

    return results


def main():
    print("=" * 50)
    print("Wave Rover Motor Calibration")
    print("=" * 50)
    print("\nMake sure:")
    print("  • Robot is on the floor")
    print("  • At least 1m clear space in front")
    print("  • You can reach the robot if needed")
    print("\nStarting in 5 seconds...")
    time.sleep(5)

    # Open rover serial for IMU
    print("\nOpening rover serial...")
    rover_ser = serial.Serial(ROVER_SERIAL, 115200, timeout=1.0)
    rover_ser.reset_input_buffer()
    enable_imu_feedback(rover_ser)

    # Open lidar
    print("Opening lidar...")
    lidar = LD19Driver(port=LIDAR_SERIAL, baudrate=230400)
    lidar.start()
    time.sleep(1.0)

    try:
        rot = calibrate_rotation(rover_ser)
        fwd = calibrate_forward(lidar)

        print("\n" + "=" * 50)
        print("CALIBRATION RESULTS")
        print("=" * 50)
        print(f"  Min spin power:  {rot.get('min_spin_power', 'N/A')}")
        print(f"  Yaw rate:        {rot.get('spin_yaw_rate_dps', 0):.1f}°/burst")
        print(f"  Min fwd power:   {fwd.get('min_fwd_power', 'N/A')}")
        print(f"  Fwd speed:       {fwd.get('fwd_speed_mps', 0):.2f}m/s (approx)")
        print("=" * 50)

    finally:
        print("\nStopping robot and closing connections...")
        send_motor_cmd(0.0, 0.0)
        lidar.stop()
        rover_ser.close()


if __name__ == "__main__":
    main()
