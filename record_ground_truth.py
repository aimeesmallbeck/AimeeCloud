#!/usr/bin/env python3
import socket
import msgpack
import time
import subprocess
import json
import os

NOTIFY = 2

class ArmRPC:
    def __init__(self, sock_path='/var/run/arduino-router.sock'):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(sock_path)
        self.sock.settimeout(5.0)
        
    def send_cartesian(self, x, y, z, pitch, gripper_w, time_ms):
        msg = [NOTIFY, "receive_cartesian", [x, y, z, pitch, gripper_w, time_ms]]
        self.sock.sendall(msgpack.packb(msg))
        
    def send_home(self, time_ms=3000):
        home_raw = [2056, 2060, 2636, 2484, 2043, 2062]
        msg = [NOTIFY, "receive_waypoints", home_raw + [time_ms]]
        self.sock.sendall(msgpack.packb(msg))

    def close(self):
        self.sock.close()

def detect_dice(label):
    ts = int(time.time())
    frame_path = f"/workspace/ground_truth_{label}_{ts}.jpg"
    
    # Ensure C++ node is active
    subprocess.run("docker exec aimee-robot bash -c 'export ROS_DOMAIN_ID=42 && source /opt/ros/humble/setup.bash && ros2 service call /arm_cam_turbo/set_active std_srvs/srv/SetBool \"{data: true}\"'", shell=True, capture_output=True)
    time.sleep(1.0)
    
    print(f"  Capturing ground truth frame for {label}...")
    grab_cmd = f"docker exec aimee-robot bash -c 'export ROS_DOMAIN_ID=42 && source /opt/ros/humble/setup.bash && python3 /workspace/grab_frame.py {frame_path}'"
    subprocess.run(grab_cmd, shell=True, capture_output=True)
    
    detect_cmd = f"docker exec aimee-robot python3 -c \"import cv2; import numpy as np; from detect_from_file import detect_dice; detect_dice('{frame_path}')\""
    result = subprocess.run(detect_cmd, shell=True, capture_output=True, text=True)
    
    if "DETECTED:" in result.stdout:
        line = [l for l in result.stdout.split('\n') if "DETECTED:" in l][0]
        coords = line.split(":")[1].split(",")
        return int(coords[0]), int(coords[1])
    return None

def main():
    import sys
    label = sys.argv[1] if len(sys.argv) > 1 else "TEST"
    
    arm = ArmRPC()
    
    # Centered further forward to cover rows 4-8
    look_x = 0.300
    look_y = 0.000
    look_z = 0.200
    pitch = 1.571
    
    print(f"--- RECORDING GROUND TRUTH FOR {label} (Height: {look_z}m) ---")
    # Move to look position (opening gripper so it doesn't block view)
    arm.send_cartesian(look_x, look_y, look_z, pitch, 0.08, 3000)
    time.sleep(3.5)
    
    pixel_pos = detect_dice(label)
    if pixel_pos:
        print(f"RESULT:{label}:{pixel_pos[0]},{pixel_pos[1]}")
    else:
        print(f"ERROR: Could not detect dice at {label}")
        
    arm.close()

if __name__ == "__main__":
    main()
