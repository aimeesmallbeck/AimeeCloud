#!/usr/bin/env python3
import socket
import msgpack
import time
import subprocess
import json
import os
import numpy as np

NOTIFY = 2

class ArmRPC:
    def __init__(self, sock_path='/var/run/arduino-router.sock'):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(sock_path)
        self.sock.settimeout(5.0)
        
    def send_cartesian(self, x, y, z, pitch, gripper_w, time_ms):
        print(f"  [RPC] Moving to X={x:.3f} Y={y:.3f} Z={z:.3f}...")
        msg = [NOTIFY, "receive_cartesian", [x, y, z, pitch, gripper_w, time_ms]]
        self.sock.sendall(msgpack.packb(msg))
        
    def send_home(self, time_ms=3000):
        home_raw = [2056, 2060, 2636, 2484, 2043, 2062]
        msg = [NOTIFY, "receive_waypoints", home_raw + [time_ms]]
        self.sock.sendall(msgpack.packb(msg))

    def close(self):
        self.sock.close()

def detect_dice():
    # Use unique filenames to defeat ANY caching
    ts = int(time.time())
    frame_path = f"/workspace/calib_frame_{ts}.jpg"
    
    # Ensure C++ node is active
    subprocess.run("docker exec aimee-robot bash -c 'export ROS_DOMAIN_ID=42 && source /opt/ros/humble/setup.bash && ros2 service call /arm_cam_turbo/set_active std_srvs/srv/SetBool \"{data: true}\"'", shell=True, capture_output=True)
    time.sleep(1.5) # Wait for hardware to stabilize
    
    print(f"  Capturing fresh frame: {frame_path}")
    # Use the unique path
    grab_cmd = f"docker exec aimee-robot bash -c 'export ROS_DOMAIN_ID=42 && source /opt/ros/humble/setup.bash && python3 /workspace/grab_frame.py {frame_path}'"
    subprocess.run(grab_cmd, shell=True, capture_output=True)
    
    # Detect using the offline detector (running logic directly to avoid import issues)
    detect_cmd = f"docker exec aimee-robot python3 -c \"import cv2; import numpy as np; from detect_from_file import detect_dice; detect_dice('{frame_path}')\""
    result = subprocess.run(detect_cmd, shell=True, capture_output=True, text=True)
    
    if "DETECTED:" in result.stdout:
        line = [l for l in result.stdout.split('\n') if "DETECTED:" in l][0]
        coords = line.split(":")[1].split(",")
        return int(coords[0]), int(coords[1])
    else:
        print(f"  DEBUG: Detection failed for {frame_path}")
        # print(f"  Output: {result.stdout}")
    return None

def main():
    arm = ArmRPC()
    calibration_data = {}
    
    # Grid parameters
    look_z = 0.100
    grasp_z = -0.075
    pitch = 1.571
    
    print("=== STARTING SELF-LEARNING CALIBRATION (HARD RESET MODE) ===")
    
    # Sample points (covering requested 4-8 range)
    test_points = [
        {"name": "4A", "x": 0.18, "y": 0.12},
        {"name": "4H", "x": 0.18, "y": -0.12},
        {"name": "8A", "x": 0.32, "y": 0.12},
        {"name": "8H", "x": 0.32, "y": -0.12}
    ]

    for pt in test_points:
        print(f"\n[POINT {pt['name']}] Targeting {pt['x']}, {pt['y']}")
        
        # 1. Place dice
        arm.send_cartesian(pt['x'], pt['y'], grasp_z, pitch, 0.005, 3000)
        time.sleep(4.0)
        arm.send_cartesian(pt['x'], pt['y'], grasp_z, pitch, 0.08, 1000) # Release
        time.sleep(1.5)
        
        # 2. Back off to 'Look'
        arm.send_cartesian(pt['x'], pt['y'], look_z, pitch, 0.08, 2000)
        time.sleep(2.5)
        
        # 3. Observe
        pixel_pos = detect_dice()
        if pixel_pos:
            u, v = pixel_pos
            du = u - 320
            dv = v - 240
            print(f"  Observed at pixel: ({u}, {v})")
            calibration_data[pt['name']] = {
                "physical_x": pt['x'], "physical_y": pt['y'],
                "pixel_u": u, "pixel_v": v
            }
        else:
            print(f"  FAILED to detect dice at {pt['name']}")

        # 4. Retrieve
        arm.send_cartesian(pt['x'], pt['y'], grasp_z, pitch, 0.005, 2000)
        time.sleep(2.5)
        arm.send_home()
        time.sleep(3.5)

    with open('grid_calibration_results.json', 'w') as f:
        json.dump(calibration_data, f, indent=2)
    
    print("\n=== CALIBRATION COMPLETE ===")
    arm.close()

if __name__ == "__main__":
    main()
