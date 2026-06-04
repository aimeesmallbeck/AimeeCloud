#!/usr/bin/env python3
import cv2
import numpy as np
import yaml
import os
import subprocess
import socket
import msgpack
import time

def detect_objects(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Character colors (excluding blue)
    color_ranges = {
        'pink': [([140, 20, 80], [180, 255, 255])],
        'green': [([40, 60, 60], [90, 255, 255])],
        'orange': [([5, 80, 80], [25, 255, 255])],
        'yellow': [([20, 60, 60], [38, 255, 255])],
        'red': [([0, 50, 50], [10, 255, 255]), ([170, 50, 50], [180, 255, 255])],
    }
    
    blue_range = ([90, 80, 50], [135, 255, 255])
    
    characters = []
    for color, ranges in color_ranges.items():
        mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for (lower, upper) in ranges:
            m = cv2.inRange(hsv, np.array(lower), np.array(upper))
            mask = cv2.bitwise_or(mask, m)
        
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 300 <= area <= 20000:
                M = cv2.moments(cnt)
                if M['m00'] > 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    max_v = np.max(cnt[:, 0, 1])
                    bottom_pixels = cnt[np.abs(cnt[:, 0, 1] - max_v) <= 3]
                    u = int(np.median(bottom_pixels[:, 0, 0]))
                    v = int(max_v)
                    characters.append({'color': color, 'center': (cx, cy), 'pick': (u, v), 'area': area, 'contour': cnt})
    
    # Sort characters by area and keep top ones
    characters.sort(key=lambda x: x['area'], reverse=True)
    # Keep top 3 if possible
    # characters = characters[:3] # User specifically said 3 characters
    
    # Detect Blue Tape
    mask = cv2.inRange(hsv, np.array(blue_range[0]), np.array(blue_range[1]))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    blue_tapes = []
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 150 <= area <= 30000:
            M = cv2.moments(cnt)
            if M['m00'] > 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                blue_tapes.append({'center': (cx, cy), 'area': area, 'contour': cnt})
                
    return characters, blue_tapes

def main():
    print("Stopping usb_cam...")
    subprocess.run(["sudo", "-S", "killall", "-9", "usb_cam_node_exe"], input=b"<REDACTED>\n")
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    time.sleep(2.0)
    
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        return
    
    cal_path = '/home/arduino/aimee-robot-ws/calibration.yaml'
    with open(cal_path, 'r') as f:
        cal = yaml.safe_load(f)
        
    chars, tapes = detect_objects(frame)
    
    print(f"Found {len(chars)} character candidates and {len(tapes)} blue tapes")
    
    # Filter characters: if multiple characters are very close, they might be the same object
    unique_chars = []
    for char in chars:
        too_close = False
        for uchar in unique_chars:
            d = np.sqrt((char['center'][0]-uchar['center'][0])**2 + (char['center'][1]-uchar['center'][1])**2)
            if d < 30:
                too_close = True
                break
        if not too_close:
            unique_chars.append(char)
            
    chars = unique_chars[:3]
    print(f"Refined to {len(chars)} unique characters")
    for i, c in enumerate(chars):
        print(f"  {i+1}: {c['color']} at {c['center']} area={c['area']}")
    
    debug = frame.copy()
    for char in chars:
        cv2.drawContours(debug, [char['contour']], -1, (0, 255, 0), 2)
        cv2.circle(debug, char['pick'], 5, (0, 0, 255), -1)
        cv2.putText(debug, char['color'], char['center'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
    for tape in tapes:
        cv2.drawContours(debug, [tape['contour']], -1, (255, 0, 0), 2)
        cv2.circle(debug, tape['center'], 5, (255, 255, 0), -1)
        
    # Identify empty tape
    empty_tape = None
    for tape in tapes:
        is_empty = True
        tx, ty = tape['center']
        for char in chars:
            cx, cy = char['center']
            dist = np.sqrt((tx-cx)**2 + (ty-cy)**2)
            if dist < 50: # Character is on this tape
                is_empty = False
                break
        if is_empty:
            empty_tape = tape
            break
            
    if empty_tape:
        print(f"Target empty tape at: {empty_tape['center']}")
        cv2.circle(debug, empty_tape['center'], 15, (0, 255, 255), 3)
    else:
        print("No empty tape found among detected tapes")
        if tapes:
            # Maybe use the one furthest from all characters
            max_min_dist = 0
            best_tape = tapes[0]
            for tape in tapes:
                min_dist = 1000
                tx, ty = tape['center']
                for char in chars:
                    cx, cy = char['center']
                    dist = np.sqrt((tx-cx)**2 + (ty-cy)**2)
                    if dist < min_dist: min_dist = dist
                if min_dist > max_min_dist:
                    max_min_dist = min_dist
                    best_tape = tape
            empty_tape = best_tape
            print(f"Selected 'best' tape at: {empty_tape['center']} (dist={max_min_dist})")
            
    cv2.imwrite('/home/arduino/scene_analysis.jpg', debug)
    print("Saved scene analysis to /home/arduino/scene_analysis.jpg")
    
    cap.release()

if __name__ == '__main__':
    main()
