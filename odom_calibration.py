#!/usr/bin/env python3
"""Odometry calibration: drive straight, compare reported vs actual distance."""
import sys, time, threading, math
sys.path.insert(0, '/workspace/install/aimee_nav/lib/python3.10/site-packages')

import rclpy
from aimee_nav.aimee_nav_node import AimeeNavNode

rclpy.init(args=[])
node = AimeeNavNode()
node._rover._http_ip = "192.168.1.56"
node._max_speed = 0.15
node._controller.max_linear = 0.15

executor = rclpy.executors.MultiThreadedExecutor()
executor.add_node(node)
t = threading.Thread(target=executor.spin, daemon=True)
t.start()

print("=" * 60)
print("ODOMETRY CALIBRATION TEST")
print("Robot will drive STRAIGHT at 0.06 m/s for 10 seconds")
print("Expected distance: ~0.6 meters (~2 feet)")
print("=" * 60)

time.sleep(2)

x0, y0, th0, _, _ = node._rover.get_odometry()
print(f"\nStart pose: x={x0:.3f}  y={y0:.3f}  theta={math.degrees(th0):.1f} deg")

print("\n[DRIVING STRAIGHT...]")
for i in range(10):
    node._rover.send_velocity(0.06, 0.0)
    time.sleep(1.0)
    x, y, th, _, _ = node._rover.get_odometry()
    dist = ((x-x0)**2 + (y-y0)**2)**0.5
    print(f"  [{i+1}s] x={x:.3f}  y={y:.3f}  theta={math.degrees(th):.1f} deg  dist={dist:.3f}")

print("\n[STOPPING]")
node._rover.stop()
time.sleep(1)
node._rover.stop()

x1, y1, th1, _, _ = node._rover.get_odometry()
dist = ((x1-x0)**2 + (y1-y0)**2)**0.5
print(f"\nFinal pose: x={x1:.3f}  y={y1:.3f}  theta={math.degrees(th1):.1f} deg")
print(f"Reported distance traveled: {dist:.3f} m")

node.destroy_node()
rclpy.shutdown()
print("\n=== TEST COMPLETE ===")
print("Please confirm: How far did the robot ACTUALLY move?")
print("Did it drive straight or curve? Any wheel slip?")
