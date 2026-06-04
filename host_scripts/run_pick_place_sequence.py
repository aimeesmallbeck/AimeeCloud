#!/usr/bin/env python3
import cv2
import numpy as np
import yaml
import os
import subprocess
import socket
import msgpack
import time
import math
import json

# ==================== Arduino Router RPC ====================
REQUEST = 0
NOTIFY = 2

def recv_response(sock):
    buf = b''
    while True:
        try:
            chunk = sock.recv(1024)
            if not chunk: return None
            buf += chunk
            unpacker = msgpack.Unpacker(raw=False, max_array_len=10, max_map_len=10)
            unpacker.feed(buf)
            return unpacker.unpack()
        except msgpack.exceptions.OutOfData: continue
        except Exception: return None

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
        
    def send_home(self, time_ms=5000):
        home_raw = [2056, 2060, 2636, 2484, 2043, 2062]
        msg = [NOTIFY, "receive_waypoints", home_raw + [time_ms]]
        packed = msgpack.packb(msg)
        self.sock.sendall(packed)
        print(f"[RPC] HOME")

    def close(self):
        self.sock.close()

# ==================== Detection Logic ====================
def detect_scene(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color_ranges = {
        'pink': [([140, 20, 80], [180, 255, 255])],
        'green': [([40, 60, 60], [90, 255, 255])],
        'orange': [([5, 80, 80], [25, 255, 255])],
        'yellow': [([20, 60, 60], [38, 255, 255])],
    }
    blue_range = ([90, 80, 50], [135, 255, 255])
    kernel = np.ones((5,5), np.uint8)
    
    characters = []
    for color, ranges in color_ranges.items():
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for (lower, upper) in ranges:
            m = cv2.inRange(hsv, np.array(lower), np.array(upper))
            mask = cv2.bitwise_or(mask, m)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 300 <= area <= 20000:
                M = cv2.moments(cnt)
                if M['m00'] > 0:
                    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                    max_v = np.max(cnt[:, 0, 1])
                    bottom_pixels = cnt[np.abs(cnt[:, 0, 1] - max_v) <= 3]
                    u, v = int(np.median(bottom_pixels[:, 0, 0])), int(max_v)
                    characters.append({'color': color, 'center': (cx, cy), 'pick': (u, v), 'area': area, 'contour': cnt})
    
    characters.sort(key=lambda x: x['area'], reverse=True)
    unique_chars = []
    for char in characters:
        if not any(np.sqrt((char['center'][0]-uchar['center'][0])**2 + (char['center'][1]-uchar['center'][1])**2) < 40 for uchar in unique_chars):
            unique_chars.append(char)
    
    mask = cv2.inRange(hsv, np.array(blue_range[0]), np.array(blue_range[1]))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    tapes = []
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 150 <= area <= 30000:
            M = cv2.moments(cnt)
            if M['m00'] > 0:
                tapes.append({'center': (int(M['m10']/M['m00']), int(M['m01']/M['m00'])), 'area': area, 'contour': cnt})
    
    return unique_chars[:3], tapes

def image_to_arm(u, v, cal):
    cx, cy = cal['image_center_x'], cal['image_center_y']
    du, dv = u - cx, cy - v
    arm_x = cal['scale_x'] * dv + cal['skew_xy'] * du + cal['offset_x']
    arm_y = cal['scale_y'] * du + cal['skew_yx'] * dv + cal['offset_y']
    return arm_x, arm_y

def main():
    print("=" * 60)
    print("3-CHARACTER PICK AND PLACE TEST")
    print("=" * 60)
    
    print("Capturing frame...")
    subprocess.run(["sudo", "-k", "-S", "killall", "-9", "usb_cam_node_exe"], input=b"<REDACTED>\n", stderr=subprocess.DEVNULL)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    time.sleep(2.0)
    cap.read(); cap.read(); ret, frame = cap.read()
    cap.release()
    if not ret: print("Error: Camera failed"); return
    
    cal_path = '/home/arduino/aimee-robot-ws/calibration.yaml'
    with open(cal_path, 'r') as f: cal = yaml.safe_load(f)
    
    chars, tapes = detect_scene(frame)
    print(f"Detected {len(chars)} characters and {len(tapes)} blue tapes")
    
    yellow_char = next((c for c in chars if c['color'] == 'yellow'), None)
    target_tape = None
    if yellow_char:
        yx, yy = yellow_char['center']
        potential_tapes = [t for t in tapes if t['center'][0] > yx + 20]
        potential_tapes.sort(key=lambda t: t['center'][0]) 
        if potential_tapes:
            target_tape = potential_tapes[0]
            print(f"Target tape (right of yellow) at {target_tape['center']}")
    
    if not target_tape and tapes:
        target_tape = tapes[0]
        print(f"Warning: Using fallback tape at {target_tape['center']}")
    
    if not target_tape: print("Error: No target tape found!"); return

    debug = frame.copy()
    for c in chars:
        cv2.drawContours(debug, [c['contour']], -1, (0, 255, 0), 2)
        cv2.putText(debug, c['color'], c['center'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.drawContours(debug, [target_tape['contour']], -1, (255, 0, 0), 3)
    cv2.imwrite('/home/arduino/pick_place_plan.jpg', debug)
    
    drop_x, drop_y = image_to_arm(target_tape['center'][0], target_tape['center'][1], cal)
    grasp_z, lift_z, safe_z, pitch = cal['desk_z'] + cal['grasp_offset'], cal['desk_z'] + cal['grasp_offset'] + cal['lift_height'], cal['safe_z'], 1.571
    t_transit, t_z, t_grip, t_home = 2666, 1733, 1333, 2200
    
    arm = ArmRPC()
    arm.send_home(t_home)
    time.sleep(2.5)
    
    for i, char in enumerate(chars):
        pick_x, pick_y = image_to_arm(char['pick'][0], char['pick'][1], cal)
        print(f"\n--- STEP {i+1}: Moving {char['color']} ---")
        arm.send_cartesian(pick_x, pick_y, safe_z, pitch, 0.08, t_transit); time.sleep(2.8)
        arm.send_cartesian(pick_x, pick_y, grasp_z, pitch, 0.08, t_z); time.sleep(1.8)
        arm.send_cartesian(pick_x, pick_y, grasp_z, pitch, 0.005, t_grip); time.sleep(1.4)
        arm.send_cartesian(pick_x, pick_y, lift_z, pitch, 0.005, t_z); time.sleep(1.8)
        arm.send_cartesian(drop_x, drop_y, lift_z, pitch, 0.005, t_transit); time.sleep(2.8)
        arm.send_cartesian(drop_x, drop_y, grasp_z, pitch, 0.005, t_z); time.sleep(1.8)
        arm.send_cartesian(drop_x, drop_y, grasp_z, pitch, 0.08, t_grip); time.sleep(1.4)
        arm.send_cartesian(drop_x, drop_y, lift_z, pitch, 0.08, t_z); time.sleep(1.8)
        
    arm.send_home(t_home); time.sleep(2.5); arm.close()
    print("DONE.")

if __name__ == '__main__':
    main()
