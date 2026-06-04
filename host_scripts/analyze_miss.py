import cv2
import numpy as np
import yaml
import math

cal_path = '/home/arduino/aimee-robot-ws/calibration.yaml'
with open(cal_path, 'r') as f:
    cal = yaml.safe_load(f)

def detect_pink(image, cal):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,
        np.array([cal['pink_hue_min'], cal['pink_sat_min'], cal['pink_val_min']]),
        np.array([cal['pink_hue_max'], cal['pink_sat_max'], cal['pink_val_max']]))
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
    
    if best is None:
        return None, None
    max_v = np.max(best[:, 0, 1])
    bottom_pixels = best[np.abs(best[:, 0, 1] - max_v) <= 3]
    u = int(np.median(bottom_pixels[:, 0, 0]))
    v = int(max_v)
    return u, v

def get_blobs(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Mask out the desk background. From GEMINI.md, desk is a specific color?
    # Let's just find anything with saturation > 100
    mask = cv2.inRange(hsv, np.array([0, 100, 50]), np.array([179, 255, 255]))
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    results = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 50:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                results.append((cX, cY, area))
    return results

image = cv2.imread('/home/arduino/miss_analysis.jpg')
pink_uv = detect_pink(image, cal)
blobs = get_blobs(image)

print(f"Pink Character: {pink_uv}")
print("Other blobs nearby:")
for b in blobs:
    if pink_uv[0] is not None:
        dist = math.hypot(b[0] - pink_uv[0], b[1] - pink_uv[1])
        if dist < 150 and dist > 5:
            print(f"  Blob at {b[0]}, {b[1]} (Area {b[2]}) - Dist: {dist:.1f}px")
            o_x, o_y = image_to_arm(b[0], b[1], cal)
            p_x, p_y = image_to_arm(pink_uv[0], pink_uv[1], cal)
            print(f"    Arm delta: dX={p_x - o_x:.4f}, dY={p_y - o_y:.4f}")

