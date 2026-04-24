#!/usr/bin/env python3
"""Goal-directed movement test. Robot WILL move."""
import sys, time, threading
sys.path.insert(0, '/workspace/install/aimee_nav/lib/python3.10/site-packages')

import rclpy
from aimee_nav.aimee_nav_node import AimeeNavNode
from geometry_msgs.msg import PoseStamped

rclpy.init(args=[])
node = AimeeNavNode()

# CRITICAL: set HTTP IP
node._rover._http_ip = "192.168.1.56"

# Safe settings for 6x6 ft space
node._max_speed = 0.15
node._controller.max_linear = 0.15
node._safety_distance = 0.50
node._enable_reactive = True
node._enable_planning = True
node._nav_mode = 'planned'

executor = rclpy.executors.MultiThreadedExecutor()
executor.add_node(node)
t = threading.Thread(target=executor.spin, daemon=True)
t.start()

print("=" * 60)
print("GOAL-DIRECTED MOVEMENT TEST")
print("Settings: max_speed=0.15 m/s, safety=0.50 m")
print("Goal: (1.0, 0.0) — straight ahead")
print("Duration: 20 seconds, then stop")
print("=" * 60)

# Wait for scan and grid population
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
print("Populating grid for 3 seconds...")
time.sleep(3)

# Send goal straight ahead
print("\n[SENDING GOAL] x=1.0, y=0.0")
goal_pub = node.create_publisher(PoseStamped, '/goal_pose', 10)
goal = PoseStamped()
goal.header.frame_id = 'map'
goal.pose.position.x = 1.0
goal.pose.position.y = 0.0
goal.pose.orientation.w = 1.0
goal_pub.publish(goal)

# Monitor
print("\nMonitoring for 20 seconds...")
for i in range(20):
    time.sleep(1.0)
    with node._state_lock:
        has_goal = node._has_goal
        path_len = len(node._path_world)
    print(f"  [{i+1:2d}s] has_goal={has_goal}  path_len={path_len}")

# Stop
print("\n[TIMEOUT] Stopping robot...")
node._rover.stop()
time.sleep(1)
node._rover.stop()

node.destroy_node()
rclpy.shutdown()
print("\n=== TEST COMPLETE ===")
print("Please confirm: Did the robot move toward the goal?")
print("Did it stop for obstacles? Did it reach approximately 1 meter forward?")
