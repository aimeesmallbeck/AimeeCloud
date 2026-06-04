#!/usr/bin/env python3
import cv2
import numpy as np
import os

MARKERS = [
    ("marker_1", 159, 207),
    ("marker_2", 362, 218),
    ("marker_3", 428, 341),
    ("marker_4", 43, 390),
]

def detect_orange_dot(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, w = img.shape[:2]
    mask = cv2.inRange(hsv, np.array([0, 60, 80]), np.array([20, 255, 255]))
    # Exclude edges
    mask[:int(h*0.10), :] = 0
    mask[:, int(w*0.70):] = 0
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    best = None
    best_score = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 3 <= area <= 100:
            perimeter = cv2.arcLength(cnt, True)
            circ = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
            score = area * (0.5 + circ)
            if score > best_score:
                best_score = score
                best = cnt
    if best is not None:
        M = cv2.moments(best)
        return int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    return None, None

print("Calibration Test Results:")
print("=" * 60)
for name, target_u, target_v in MARKERS:
    fname = f'/workspace/calib_test_{name}.jpg'
    if not os.path.exists(fname):
        print(f'{name}: IMAGE NOT FOUND')
        continue
    img = cv2.imread(fname)
    u, v = detect_orange_dot(img)
    if u is not None:
        du = u - target_u
        dv = v - target_v
        dist = np.sqrt(du**2 + dv**2)
        print(f'{name}: target=({target_u},{target_v}) dot=({u},{v}) error=({du:+d},{dv:+d}) dist={dist:.1f}px')
        
        # Compute arm error from pixel error
        # dX/dv ≈ -0.000662, dY/du ≈ -0.000598
        dx = -0.000662 * dv
        dy = -0.000598 * du
        arm_err = np.sqrt(dx**2 + dy**2)
        print(f'       -> estimated arm error: dx={dx*1000:+.1f}mm, dy={dy*1000:+.1f}mm, total={arm_err*1000:.1f}mm')
    else:
        print(f'{name}: target=({target_u},{target_v}) NO ORANGE DOT DETECTED')
print("=" * 60)
