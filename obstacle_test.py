#!/usr/bin/env python3
"""Obstacle avoidance test. Robot WILL move."""
import sys, time, threading
sys.path.insert(0, '/workspace/install/aimee_nav/lib/python3.10/site-packages')

import rclpy
from rclpy.parameter import Parameter
from aimee_nav.aimee_nav_node import AimeeNavNode

rclpy.init(args=[])
node = AimeeNavNode(parameter_overrides=[
    Parameter('rover_http_ip', Parameter.Type.STRING, '192.168.1.56'),
    Parameter('max_speed', Parameter.Type.DOUBLE, 0.15),
    Parameter('safety_distance_m', Parameter.Type.DOUBLE, 0.60),
    Parameter('enable_reactive', Parameter.Type.BOOL, True),
    Parameter('enable_planning', Parameter.Type.BOOL, False),
    Parameter('angular_scale', Parameter.Type.DOUBLE, 4.0),
    Parameter('nav_rate_hz', Parameter.Type.DOUBLE, 5.0),
    Parameter('publish_decimation', Parameter.Type.INTEGER, 100),
])

# Controller limit is not exposed as a ROS parameter
node._controller.max_linear = 0.15

executor = rclpy.executors.MultiThreadedExecutor()
executor.add_node(node)
t = threading.Thread(target=executor.spin, daemon=True)
t.start()

print("=" * 60)
print("OBSTACLE AVOIDANCE TEST")
print("Obstacle placed ~1 meter in front")
print("Settings: max_speed=0.15 m/s, safety=0.60 m")
print("Duration: 15 seconds, then stop")
print("=" * 60)

# Wait for scan
print("\nWaiting for scan...")
for i in range(20):
    if node._latest_scan is not None:
        break
    time.sleep(0.5)

if node._latest_scan is None:
    print("No scan — aborting.")
    node.destroy_node()
    rclpy.shutdown()
    sys.exit(1)

print(f"Scan ready ({len(node._latest_scan.points)} points).")
print("\nMonitoring front sector and commands for 15 seconds...")
print("-" * 60)

for i in range(15):
    time.sleep(1.0)
    
    # Get sector info
    with node._state_lock:
        scan = node._latest_scan
    
    if scan:
        points = list(zip(
            [p.angle_deg for p in scan.points],
            [p.distance_m for p in scan.points],
            [p.intensity for p in scan.points]
        ))
        sectors = node._avoidance.analyze_sectors(points)
        front = next((s for s in sectors if s.name == 'front'), None)
        fl = next((s for s in sectors if s.name == 'front_left'), None)
        fr = next((s for s in sectors if s.name == 'front_right'), None)
        
        front_dist = front.min_distance if front else float('inf')
        fl_dist = fl.min_distance if fl else float('inf')
        fr_dist = fr.min_distance if fr else float('inf')
        front_blocked = front.is_blocked if front else False
    else:
        front_dist = fl_dist = fr_dist = float('inf')
        front_blocked = False
    
    print(f"  [{i+1:2d}s] front={front_dist:.2f}m  fl={fl_dist:.2f}m  fr={fr_dist:.2f}m  blocked={front_blocked}")

# Stop
print("\n[TIMEOUT] Stopping robot...")
node._rover.stop()
time.sleep(1)
node._rover.stop()

node.destroy_node()
rclpy.shutdown()
print("\n=== TEST COMPLETE ===")
print("Please confirm:")
print("  - Did the robot detect the obstacle and stop?")
print("  - Did it turn to avoid it?")
print("  - How close did it get to the obstacle?")
