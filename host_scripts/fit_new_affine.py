#!/usr/bin/env python3
import json
import numpy as np
import yaml
import math

CAL_FILE = '/home/arduino/new_calibration_points.json'
YAML_FILE = '/home/arduino/aimee-robot-ws/calibration.yaml'

with open(CAL_FILE, 'r') as f:
    data = json.load(f)

points = data['points']
if len(points) < 3:
    print("Need at least 3 points for affine fit.")
    exit(1)

image_center_x = 320.0
image_center_y = 240.0

A = []
B_x = []
B_y = []

for pt in points:
    u, v = pt['u'], pt['v']
    arm_x, arm_y = pt['x'], pt['y']
    du = u - image_center_x
    dv = image_center_y - v
    A.append([dv, du, 1])
    B_x.append(arm_x)
    B_y.append(arm_y)

A = np.array(A)
B_x = np.array(B_x)
B_y = np.array(B_y)

x_params, _, _, _ = np.linalg.lstsq(A, B_x, rcond=None)
scale_x, skew_xy, offset_x = x_params

A_y = []
for pt in points:
    du = pt['u'] - image_center_x
    dv = image_center_y - pt['v']
    A_y.append([du, dv, 1])
A_y = np.array(A_y)

y_params, _, _, _ = np.linalg.lstsq(A_y, B_y, rcond=None)
scale_y, skew_yx, offset_y = y_params

print("\n--- Fit Results ---")
print(f"scale_x: {scale_x:.6f}")
print(f"offset_x: {offset_x:.6f}")
print(f"skew_xy: {skew_xy:.6f}")
print(f"scale_y: {scale_y:.6f}")
print(f"offset_y: {offset_y:.6f}")
print(f"skew_yx: {skew_yx:.6f}")

print("\n--- Residuals ---")
for i, pt in enumerate(points):
    u, v = pt['u'], pt['v']
    du = u - image_center_x
    dv = image_center_y - v
    pred_x = scale_x * dv + skew_xy * du + offset_x
    pred_y = scale_y * du + skew_yx * dv + offset_y
    err_x = pred_x - B_x[i]
    err_y = pred_y - B_y[i]
    err_dist = math.hypot(err_x, err_y)
    print(f"Pt {i+1}: dx={err_x*1000:+.1f}mm, dy={err_y*1000:+.1f}mm, dist={err_dist*1000:.1f}mm")

# Update YAML
with open(YAML_FILE, 'r') as f:
    cal = yaml.safe_load(f)

cal['scale_x'] = float(scale_x)
cal['offset_x'] = float(offset_x)
cal['skew_xy'] = float(skew_xy)
cal['scale_y'] = float(scale_y)
cal['offset_y'] = float(offset_y)
cal['skew_yx'] = float(skew_yx)

with open(YAML_FILE, 'w') as f:
    yaml.dump(cal, f, default_flow_style=False)

print("\nUpdated calibration.yaml successfully.")
