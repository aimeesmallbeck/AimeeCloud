#!/usr/bin/env python3
import socket
import msgpack
import time

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
        # Home position waypoints (safe defaults)
        home_raw = [2056, 2060, 2636, 2484, 2043, 2062]
        msg = [NOTIFY, "receive_waypoints", home_raw + [time_ms]]
        packed = msgpack.packb(msg)
        self.sock.sendall(packed)
        print(f"[RPC] HOME")

    def close(self):
        self.sock.close()

def main():
    arm = ArmRPC()
    
    # Place coordinates (relative to shoulder link)
    # Using a safe forward position
    place_x = 0.250
    place_y = 0.000
    place_z = -0.055 # desk_z (-0.075) + grasp_offset (0.02)
    safe_z = 0.05
    pitch = 1.571 # Straight down
    
    print("--- Executing PLACE Sequence ---")
    
    # 1. Transit to above place location
    print("Step 1: Moving above placement location...")
    arm.send_cartesian(place_x, place_y, safe_z, pitch, 0.005, 3000)
    time.sleep(3.5)
    
    # 2. Lower to desk
    print("Step 2: Lowering to desk...")
    arm.send_cartesian(place_x, place_y, place_z, pitch, 0.005, 2000)
    time.sleep(2.5)
    
    # 3. Open gripper
    print("Step 3: Releasing dice...")
    arm.send_cartesian(place_x, place_y, place_z, pitch, 0.08, 1500)
    time.sleep(2.0)
    
    # 4. Lift to safe height
    print("Step 4: Lifting...")
    arm.send_cartesian(place_x, place_y, safe_z, pitch, 0.08, 2000)
    time.sleep(2.5)
    
    # 5. Return Home
    print("Step 5: Returning Home...")
    arm.send_home(3000)
    time.sleep(3.5)
    
    print("--- PLACE Sequence Complete ---")
    arm.close()

if __name__ == "__main__":
    main()
