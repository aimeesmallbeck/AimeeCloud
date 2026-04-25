#!/usr/bin/env python3
"""Diagnostic: find angle of closest obstacle to determine lidar mounting orientation."""
import sys, time
sys.path.insert(0, '/workspace/install/aimee_nav/lib/python3.10/site-packages')

import rclpy
from rclpy.parameter import Parameter
from aimee_nav.aimee_nav_node import AimeeNavNode

rclpy.init(args=[])
node = AimeeNavNode(parameter_overrides=[
    Parameter('rover_http_ip', Parameter.Type.STRING, '192.168.1.56'),
    Parameter('enable_reactive', Parameter.Type.BOOL, False),
    Parameter('enable_planning', Parameter.Type.BOOL, False),
    Parameter('nav_rate_hz', Parameter.Type.DOUBLE, 2.0),
    Parameter('publish_decimation', Parameter.Type.INTEGER, 100),
])

print("Place an obstacle DIRECTLY in front of the robot (~0.5 m).")
print("Waiting for scan...")

for i in range(30):
    if node._latest_scan is not None:
        break
    time.sleep(0.5)

if node._latest_scan is None:
    print("No scan received — aborting.")
    node.destroy_node()
    rclpy.shutdown()
    sys.exit(1)

scan = node._latest_scan
points = sorted(scan.points, key=lambda p: p.distance_m)

print(f"\nScan has {len(scan.points)} points.")
print("Closest 10 points:")
for i, p in enumerate(points[:10]):
    print(f"  {i+1}. angle={p.angle_deg:6.1f}°  dist={p.distance_m:.2f}m  intensity={p.intensity}")

# Find the closest point in the front 60° wedge (-30° to +30°)
front_points = [p for p in scan.points if -30 <= ((p.angle_deg + 180) % 360) - 180 <= 30]
if front_points:
    closest_front = min(front_points, key=lambda p: p.distance_m)
    print(f"\nClosest point in FRONT sector (-30°..+30°): angle={closest_front.angle_deg:.1f}°  dist={closest_front.distance_m:.2f}m")
else:
    print("\nNo points in FRONT sector (-30°..+30°)!")

node.destroy_node()
rclpy.shutdown()

print("\nInterpretation:")
print("  - If closest obstacle is near angle ~0°,   lidar is aligned correctly.")
print("  - If closest obstacle is near angle ~180°,  lidar is mounted BACKWARDS.")
print("  - If closest obstacle is near angle ~90°,   lidar is mounted rotated +90°.")
print("  - If closest obstacle is near angle ~-90°,  lidar is mounted rotated -90°.")
