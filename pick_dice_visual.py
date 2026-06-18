#!/usr/bin/env python3
import socket
import msgpack
import time
import subprocess
import os

NOTIFY = 2

class ArmRPC:
    def __init__(self, sock_path='/var/run/arduino-router.sock'):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(sock_path)
        self.sock.settimeout(5.0)
        print(f"[RPC] Connected to {sock_path}")
        
    def send_cartesian(self, x, y, z, pitch, gripper_w, time_ms):
        msg = [NOTIFY, "receive_cartesian", [x, y, z, pitch, gripper_w, time_ms]]
        packed = msgpack.packb(msg)
        self.sock.sendall(packed)
        print(f"[RPC] CARTESIAN x={x:.4f} y={y:.4f} z={z:.4f} pitch={pitch:.3f} gripper={gripper_w:.3f} t={time_ms}ms")
        
    def send_home(self, time_ms=3000):
        home_raw = [2056, 2060, 2636, 2484, 2043, 2062]
        msg = [NOTIFY, "receive_waypoints", home_raw + [time_ms]]
        packed = msgpack.packb(msg)
        self.sock.sendall(packed)
        print(f"[RPC] HOME")

    def close(self):
        self.sock.close()

def main():
    arm = ArmRPC()
    
    # 1. Move to look position
    # Raised look_z from 0.050 to 0.100 (approx 4 inches higher) for better field of view
    look_x = 0.250
    look_y = 0.000
    look_z = 0.100 
    pitch = 1.571 # Looking straight down
    
    print("--- STEP 1: Moving to LOOK position ---")
    arm.send_cartesian(look_x, look_y, look_z, pitch, 0.08, 3000)
    time.sleep(3.5)
    
    # 2. Run detection using the new C++ node
    print("--- STEP 2: Capturing and detecting red dice (C++ Turbo) ---")
    
    # Ensure C++ node is active
    subprocess.run("docker exec aimee-robot bash -c 'export ROS_DOMAIN_ID=42 && source /opt/ros/humble/setup.bash && ros2 service call /arm_cam_turbo/set_active std_srvs/srv/SetBool \"{data: true}\"'", shell=True)
    time.sleep(1.0)
    
    # Use the new grab_frame.py to fetch from the /compressed topic (High efficiency)
    grab_cmd = "docker exec aimee-robot bash -c 'export ROS_DOMAIN_ID=42 && source /opt/ros/humble/setup.bash && python3 /workspace/grab_frame.py /workspace/dice_pick_frame.jpg'"
    subprocess.run(grab_cmd, shell=True)
    
    # Detect using the offline detector script
    result = subprocess.run("docker exec aimee-robot python3 /workspace/detect_from_file.py", shell=True, capture_output=True, text=True)
    
    print("Detection Output:")
    print(result.stdout)
    
    if "DETECTED:" not in result.stdout:
        print("ERROR: Dice not detected!")
        arm.close()
        return

    # Parse coordinates
    line = [l for l in result.stdout.split('\n') if "DETECTED:" in l][0]
    coords = line.split(":")[1].split(",")
    u, v = int(coords[0]), int(coords[1])
    print(f"Dice found at pixel: ({u}, {v})")
    
    # 3. Calculate Move (Relative)
    # Image is 640x480. Center is (320, 240).
    du = u - 320
    dv = v - 240
    
    # Heuristic update: At z=0.100, the pixels cover more area.
    # Previous scale was 0.0004 at z=0.050.
    # At double height, we likely need a larger scale. 
    # Approx 0.0008 per pixel?
    scale = 0.0008 
    dy = -du * scale 
    dx = dv * scale  
    
    # Maintaining the 1.25cm fixed extension
    target_x = look_x + dx + 0.0125 
    target_y = look_y + dy

    print(f"Offset: du={du}, dv={dv} -> dx={dx:.4f}, dy={dy:.4f}")
    print(f"Target: x={target_x:.4f}, y={target_y:.4f}")

    # 4. PICK
    print("--- STEP 3: Executing PICK sequence ---")
    # Adjusting grasp_z from -0.055 to -0.075 based on feedback
    grasp_z = -0.075 
    safe_z = 0.05

    # Center over dice
    arm.send_cartesian(target_x, target_y, safe_z, pitch, 0.08, 2000)
    time.sleep(2.5)

    # Restart camera node for monitor in background BEFORE move to see it in action
    # Using very low fps to stay safe
    restart_cmd = "docker exec aimee-robot bash -c 'export ROS_DOMAIN_ID=42 && source /opt/ros/humble/setup.bash && source /workspace/install/setup.bash && ros2 run v4l2_camera v4l2_camera_node --ros-args -p video_device:=/dev/video0 -p image_size:=[640,480] -p time_per_frame:=[1,5] -r image_raw:=/vision/arm_camera/image_raw' > /dev/null 2>&1 &"
    subprocess.run(restart_cmd, shell=True)
    time.sleep(2.0)

    # Lower
    arm.send_cartesian(target_x, target_y, grasp_z, pitch, 0.08, 2000)
    time.sleep(2.5)

    # Close (Tightening from 0.010 to 0.005 for maximum grip)
    arm.send_cartesian(target_x, target_y, grasp_z, pitch, 0.005, 1500)
    time.sleep(2.0)

    
    # Lift
    arm.send_cartesian(target_x, target_y, safe_z, pitch, 0.02, 2000)
    time.sleep(2.5)
    
    # Home
    arm.send_home(3000)
    time.sleep(3.5)
    
    print("--- PICK Sequence Complete ---")
    arm.close()

if __name__ == "__main__":
    main()
