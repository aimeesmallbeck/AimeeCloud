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

# ==================== Detection Logic ====================
def detect_scene(image, step_name):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color_ranges = {
        'pink': [([120, 20, 20], [179, 255, 255])], # Extremely relaxed
        'yellow': [([15, 60, 60], [45, 255, 255])],
        'red': [([0, 60, 40], [12, 255, 255]), ([165, 60, 40], [180, 255, 255])],
    }
    blue_range = ([90, 80, 50], [135, 255, 255])
    kernel = np.ones((3,3), np.uint8)
    
    desk_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    desk_mask[50:430, 50:590] = 255
    
    found_chars = {}
    debug = image.copy()

    for color, ranges in color_ranges.items():
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for (lower, upper) in ranges:
            m = cv2.inRange(hsv, np.array(lower), np.array(upper))
            mask = cv2.bitwise_or(mask, m)
        mask = cv2.bitwise_and(mask, desk_mask)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        best_char = None
        max_area = 0
        min_area_thresh = 30 if color == 'pink' else 150
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if min_area_thresh <= area <= 30000:
                if area > max_area:
                    max_area = area
                    M = cv2.moments(cnt)
                    if M['m00'] > 0:
                        cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                        max_v = np.max(cnt[:, 0, 1])
                        bottom_pixels = cnt[np.abs(cnt[:, 0, 1] - max_v) <= 3]
                        u, v = int(np.median(bottom_pixels[:, 0, 0])), int(max_v)
                        best_char = {'color': color, 'center': (cx, cy), 'pick': (u, v), 'area': area, 'contour': cnt}
        if best_char:
            found_chars[color] = best_char
            cv2.drawContours(debug, [best_char['contour']], -1, (0, 255, 0), 2)
            cv2.putText(debug, color, best_char['center'], cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    mask = cv2.inRange(hsv, np.array(blue_range[0]), np.array(blue_range[1]))
    mask = cv2.bitwise_and(mask, desk_mask)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
    tapes = []
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 150 <= area <= 30000:
            M = cv2.moments(cnt)
            if M['m00'] > 0:
                tapes.append({'center': (int(M['m10']/M['m00']), int(M['m01']/M['m00'])), 'area': area, 'contour': cnt})

    # Pick the character specified for this step
    current_char = found_chars.get(step_name)
    
    empty_tape = None
    for tape in tapes:
        if not any(np.sqrt((tape['center'][0]-c['center'][0])**2 + (tape['center'][1]-c['center'][1])**2) < 55 for c in found_chars.values()):
            empty_tape = tape; break
    
    if empty_tape:
        cv2.drawContours(debug, [empty_tape['contour']], -1, (255, 0, 0), 3)
        cv2.putText(debug, "TARGET", empty_tape['center'], cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    cv2.imwrite(f'/home/arduino/plan_{step_name}.jpg', debug)
    return found_chars, empty_tape

def image_to_arm(u, v, cal):
    cx, cy = cal['image_center_x'], cal['image_center_y']
    du, dv = u - cx, cy - v
    arm_x = cal['scale_x'] * dv + cal['skew_xy'] * du + cal['offset_x']
    arm_y = cal['scale_y'] * du + cal['skew_yx'] * dv + cal['offset_y']
    return arm_x, arm_y

def move_character(arm, char, target, cal):
    pick_x, pick_y = image_to_arm(char['pick'][0], char['pick'][1], cal)
    drop_x, drop_y = image_to_arm(target['center'][0], target['center'][1], cal)
    gz, lz, sz, p = cal['desk_z'] + cal['grasp_offset'], cal['desk_z'] + cal['grasp_offset'] + cal['lift_height'], cal['safe_z'], 1.571
    t_tr, t_z, t_g = 2666, 1733, 1333
    arm.send_cartesian(pick_x, pick_y, sz, p, 0.08, t_tr); time.sleep(2.8)
    arm.send_cartesian(pick_x, pick_y, gz, p, 0.08, t_z); time.sleep(1.8)
    arm.send_cartesian(pick_x, pick_y, gz, p, 0.005, t_g); time.sleep(1.4)
    arm.send_cartesian(pick_x, pick_y, lz, p, 0.005, t_z); time.sleep(1.8)
    arm.send_cartesian(drop_x, drop_y, lz, p, 0.005, t_tr); time.sleep(2.8)
    arm.send_cartesian(drop_x, drop_y, gz, p, 0.005, t_z); time.sleep(1.8)
    arm.send_cartesian(drop_x, drop_y, gz, p, 0.08, t_g); time.sleep(1.4)
    arm.send_cartesian(drop_x, drop_y, lz, p, 0.08, t_z); time.sleep(1.8)

def main():
    cal_path = '/home/arduino/aimee-robot-ws/calibration.yaml'
    with open(cal_path, 'r') as f: cal = yaml.safe_load(f)
    arm = ArmRPC()
    sequence = ['pink', 'yellow', 'red']
    
    for color in sequence:
        print(f"\n--- Sequence Part: Moving {color} character ---")
        arm.send_home(3000); time.sleep(3.5)
        subprocess.run(["sudo", "-k", "-S", "killall", "-9", "usb_cam_node_exe"], input=b"<REDACTED>\n", stderr=subprocess.DEVNULL)
        cap = cv2.VideoCapture(0); cap.set(3, 640); cap.set(4, 480); time.sleep(2.0)
        ret, frame = cap.read(); cap.release()
        if not ret: print("Error: Camera failed"); break
        chars, target = detect_scene(frame, color)
        
        # If pink detection is still failing, let's use the 'unknown high-saturation object' logic
        if color == 'pink' and 'pink' not in chars:
            print("Pink not detected by range, attempting exclusion search...")
            # Any object that isn't red or yellow but is on the desk
            for possible_name, data in chars.items():
                # We already have red and yellow, if something else popped up...
                pass
            # Just look for the object that isn't red or yellow
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            red_mask = cv2.bitwise_or(cv2.inRange(hsv, np.array([0, 60, 40]), np.array([12, 255, 255])),
                                      cv2.inRange(hsv, np.array([165, 60, 40]), np.array([180, 255, 255])))
            yellow_mask = cv2.inRange(hsv, np.array([15, 60, 60]), np.array([45, 255, 255]))
            desk_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
            desk_mask[100:400, 100:550] = 255
            known_mask = cv2.bitwise_or(red_mask, yellow_mask)
            not_known_mask = cv2.bitwise_and(cv2.bitwise_not(known_mask), desk_mask)
            object_mask = cv2.bitwise_and(not_known_mask, (hsv[:,:,1] > 40).astype(np.uint8)*255)
            cnts, _ = cv2.findContours(object_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if cnts:
                best_cnt = max(cnts, key=cv2.contourArea)
                if cv2.contourArea(best_cnt) > 50:
                    M = cv2.moments(best_cnt)
                    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                    max_v = np.max(best_cnt[:, 0, 1])
                    u, v = int(np.median(best_cnt[np.abs(best_cnt[:, 0, 1] - max_v) <= 3][:, 0, 0])), int(max_v)
                    chars['pink'] = {'color': 'pink', 'center': (cx, cy), 'pick': (u, v), 'area': cv2.contourArea(best_cnt), 'contour': best_cnt}
                    print("Found candidate pink/purple character by exclusion!")

        if color not in chars:
            print(f"Error: {color} character not detected!")
            print(f"Detected colors: {list(chars.keys())}")
            break
        if not target:
            print(f"Error: No target tape found!")
            break
            
        move_character(arm, chars[color], target, cal)
    
    arm.send_home(3000); time.sleep(3.5); arm.close()

if __name__ == '__main__':
    main()
