#!/usr/bin/env python3
import sys
import json
import os
import cv2
import numpy as np
import time
import socket
import msgpack
import math

CAL_FILE = '/home/arduino/new_calibration_points.json'

def raw_to_rad(raw, offset=2047, mult=1.0):
    return (raw - offset) * math.pi / 2048.0 * mult

def fk(s_raw, e_raw, w_raw):
    s_rad = raw_to_rad(s_raw, 2047, 1.0)
    e_rad = raw_to_rad(e_raw, 1024, 1.0)
    w_rad = raw_to_rad(w_raw, 2047, 1.0)
    l2, t2rad, l3, lE, tErad = 0.23871, 0.1259, 0.14449, 0.17221, 0.0795
    angle2 = math.pi/2 - (s_rad + t2rad)
    aOut = l2 * math.cos(angle2)
    bOut = l2 * math.sin(angle2)
    angle3 = math.pi/2 - (e_rad + s_rad)
    cOut = l3 * math.cos(angle3)
    dOut = l3 * math.sin(angle3)
    angleE = math.pi/2 - (e_rad + s_rad + w_rad + tErad)
    eOut = lE * math.cos(angleE)
    fOut = lE * math.sin(angleE)
    return aOut + cOut + eOut, bOut + dOut + fOut

def fk_full(joints):
    j1, j2, j3, j4 = joints[0], joints[1], joints[3], joints[4]
    yaw = (2047 - j1) * math.pi / 2048.0
    r_ee, z_ee = fk(j2, j3, j4)
    x = r_ee * math.cos(yaw)
    y = r_ee * math.sin(yaw)
    z = z_ee + 0.12606
    return x, y, z

def detect_pink(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([140, 15, 80]), np.array([180, 255, 255]))
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best = None
    best_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > best_area:
            best_area = area
            best = cnt
    if best is None: return None, None
    max_v = np.max(best[:, 0, 1])
    bottom_pixels = best[np.abs(best[:, 0, 1] - max_v) <= 3]
    u = int(np.median(bottom_pixels[:, 0, 0]))
    v = int(max_v)
    return u, v

def read_arm():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect('/var/run/arduino-router.sock')
        sock.settimeout(5.0)
        sock.sendall(msgpack.packb([0, 999, "read_arm_positions", []]))
        buf = b''
        while True:
            chunk = sock.recv(1024)
            if not chunk: break
            buf += chunk
            try:
                unpacker = msgpack.Unpacker(raw=False)
                unpacker.feed(buf)
                resp = unpacker.unpack()
                if resp and len(resp) >= 4 and resp[3] != "ERROR":
                    return [int(x) for x in resp[3].split(",")]
            except:
                continue
    except:
        pass
    finally:
        sock.close()
    return None

def freeze_arm():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect('/var/run/arduino-router.sock')
        sock.sendall(msgpack.packb([0, 998, "freeze_arm", []]))
    except: pass
    finally: sock.close()

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    
    if cmd == "freeze":
        freeze_arm()
        print("Arm is now limp. Move it manually.")
    
    elif cmd == "capture_image":
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        time.sleep(1.0)
        cap.read()
        cap.read()
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            print("Failed to capture image.")
            sys.exit(1)
            
        u, v = detect_pink(frame)
        if u is None:
            print("No pink character found!")
            sys.exit(1)
            
        cv2.circle(frame, (u, v), 5, (0, 255, 0), -1)
        cv2.imwrite('/home/arduino/cal_frame.jpg', frame)
        print(f"Captured pink character at u={u}, v={v}")
        
        data = {}
        if os.path.exists(CAL_FILE):
            with open(CAL_FILE, 'r') as f: data = json.load(f)
        data['current_uv'] = [u, v]
        with open(CAL_FILE, 'w') as f: json.dump(data, f)
        
    elif cmd == "record_arm":
        joints = read_arm()
        if not joints:
            print("Failed to read arm.")
            sys.exit(1)
            
        x, y, z = fk_full(joints)
        print(f"Arm recorded at X={x:.4f}, Y={y:.4f}, Z={z:.4f}")
        
        data = {}
        if os.path.exists(CAL_FILE):
            with open(CAL_FILE, 'r') as f: data = json.load(f)
            
        if 'current_uv' not in data:
            print("No image capture found!")
            sys.exit(1)
            
        uv = data['current_uv']
        if 'points' not in data: data['points'] = []
        data['points'].append({'u': uv[0], 'v': uv[1], 'x': x, 'y': y, 'joints': joints})
        del data['current_uv']
        
        with open(CAL_FILE, 'w') as f: json.dump(data, f, indent=2)
        print(f"Saved point {len(data['points'])}. Ready for next.")
    else:
        print("Usage: calibrate_step.py [freeze | capture_image | record_arm]")
