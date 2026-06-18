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
        print(f"  [RPC] Moving to X={x:.4f} Y={y:.4f} Z={z:.4f}...")
        msg = [NOTIFY, "receive_cartesian", [x, y, z, pitch, gripper_w, time_ms]]
        self.sock.sendall(msgpack.packb(msg))
        
    def send_home(self, time_ms=3000):
        home_raw = [2056, 2060, 2636, 2484, 2043, 2062]
        msg = [NOTIFY, "receive_waypoints", home_raw + [time_ms]]
        self.sock.sendall(msgpack.packb(msg))

    def close(self):
        self.sock.close()

def load_calibration():
    # Load from the host directory where the script is executed
    script_dir = os.path.dirname(os.path.abspath(__file__))
    calib_path = os.path.join(script_dir, 'vision_calibration.json')
    try:
        with open(calib_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Could not load calibration from {calib_path}: {e}")
        return None

def pixel_to_physical(u, v, transform_matrix):
    M = np.array(transform_matrix)
    pt_3d = np.array([u, v, 1.0])
    mapped = np.dot(M, pt_3d)
    x = mapped[0] / mapped[2]
    y = mapped[1] / mapped[2]
    return x, y

def detect_dice():
    ts = int(time.time())
    frame_path = f"/workspace/smart_pick_frame_{ts}.jpg"
    
    # Ensure C++ node is active
    subprocess.run("docker exec aimee-robot bash -c 'export ROS_DOMAIN_ID=42 && source /opt/ros/humble/setup.bash && ros2 service call /arm_cam_turbo/set_active std_srvs/srv/SetBool \"{data: true}\"'", shell=True, capture_output=True)
    time.sleep(1.0)
    
    print(f"  Capturing frame for smart pick...")
    grab_cmd = f"docker exec aimee-robot bash -c 'export ROS_DOMAIN_ID=42 && source /opt/ros/humble/setup.bash && python3 /workspace/grab_frame.py {frame_path}'"
    subprocess.run(grab_cmd, shell=True, capture_output=True)
    
    detect_cmd = f"docker exec aimee-robot python3 -c \"import cv2; import numpy as np; from detect_from_file import detect_dice; detect_dice('{frame_path}')\""
    result = subprocess.run(detect_cmd, shell=True, capture_output=True, text=True)
    
    # Free bus
    subprocess.run("docker exec aimee-robot bash -c 'export ROS_DOMAIN_ID=42 && source /opt/ros/humble/setup.bash && ros2 service call /arm_cam_turbo/set_active std_srvs/srv/SetBool \"{data: false}\"'", shell=True, capture_output=True)

    if "DETECTED:" in result.stdout:
        line = [l for l in result.stdout.split('\n') if "DETECTED:" in l][0]
        coords = line.split(":")[1].split(",")
        return int(coords[0]), int(coords[1])
    return None

def main():
    import sys
    
    calib = load_calibration()
    if not calib:
        return
        
    arm = ArmRPC()
    
    # Standard parameters from calibration
    look_x = calib["look_x"]
    look_y = calib["look_y"]
    look_z = calib["look_z"]
    pitch = calib["pitch"]
    grasp_z = -0.075
    safe_z = 0.050
    
    print("=== SMART PICK SEQUENCE ===")
    
    # 1. Move to calibrated look position
    print("Step 1: Moving to Look Position")
    arm.send_cartesian(look_x, look_y, look_z, pitch, 0.08, 3000)
    time.sleep(3.5)
    
    # 2. Detect and calculate true physical coordinate
    print("Step 2: Detecting Target")
    pixel = detect_dice()
    if not pixel:
        print("ERROR: Dice not found. Aborting.")
        arm.close()
        return
        
    target_x, target_y = pixel_to_physical(pixel[0], pixel[1], calib["transform_matrix"])
    print(f"  Target located at Pixel: ({pixel[0]}, {pixel[1]}) -> Physical: X={target_x:.4f}, Y={target_y:.4f}")
    
    # 3. Execute Pick
    print("Step 3: Executing Pick")
    
    # Center over dice
    arm.send_cartesian(target_x, target_y, safe_z, pitch, 0.08, 2000)
    time.sleep(2.5)
    
    # Lower
    arm.send_cartesian(target_x, target_y, grasp_z, pitch, 0.08, 2000)
    time.sleep(2.5)
    
    # Close (Tight grip)
    arm.send_cartesian(target_x, target_y, grasp_z, pitch, 0.005, 1500)
    time.sleep(2.0)
    
    # Lift
    arm.send_cartesian(target_x, target_y, safe_z, pitch, 0.005, 2000)
    time.sleep(2.5)
    
    # Home
    arm.send_home(3000)
    time.sleep(3.5)
    
    print("=== SEQUENCE COMPLETE ===")
    arm.close()

if __name__ == "__main__":
    main()
