#!/usr/bin/env python3
import cv2
import numpy as np
import os

MARKERS = [
    ("marker_1", 159, 207, 0.295, 0.022),
    ("marker_2", 362, 218, 0.287, -0.099),
    ("marker_3", 428, 341, 0.206, -0.139),
    ("marker_4", 43, 390, 0.174, 0.092),
]

for name, tu, tv, tx, ty in MARKERS:
    fname = f'/workspace/calib_test_{name}.jpg'
    if not os.path.exists(fname):
        print(f'{name}: NOT FOUND')
        continue
    img = cv2.imread(fname)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Sample at expected dot position (from calibration: same as marker)
    eu, ev = tu, tv
    if 0 <= eu < img.shape[1] and 0 <= ev < img.shape[0]:
        hsv_exp = hsv[ev, eu]
        bgr_exp = img[ev, eu]
    else:
        hsv_exp = bgr_exp = None
    
    # Sample at detected "dot" positions (bottom of image)
    # Check a few candidates near where false positives appeared
    candidates = [(240, 445), (212, 425), (173, 425), (226, 445)]
    
    print(f'\n=== {name}: cmd=({tx:.3f},{ty:+.3f}) ===')
    print(f'Expected dot at ({eu},{ev}):')
    if hsv_exp is not None:
        print(f'  HSV=({hsv_exp[0]},{hsv_exp[1]},{hsv_exp[2]}) BGR=({bgr_exp[0]},{bgr_exp[1]},{bgr_exp[2]})')
    
    # Also sample a 5x5 patch around expected position
    patch = []
    for du in range(-2, 3):
        for dv in range(-2, 3):
            u, v = eu+du, ev+dv
            if 0 <= u < img.shape[1] and 0 <= v < img.shape[0]:
                patch.append(hsv[v, u])
    if patch:
        patch = np.array(patch)
        print(f'  5x5 patch H mean={patch[:,0].mean():.1f} S mean={patch[:,1].mean():.1f} V mean={patch[:,2].mean():.1f}')
    
    print('Candidate bottom positions:')
    for cu, cv in candidates:
        if 0 <= cu < img.shape[1] and 0 <= cv < img.shape[0]:
            hsv_c = hsv[cv, cu]
            bgr_c = img[cv, cu]
            print(f'  ({cu},{cv}): HSV=({hsv_c[0]},{hsv_c[1]},{hsv_c[2]}) BGR=({bgr_c[0]},{bgr_c[1]},{bgr_c[2]})')
    
    # Find best orange candidate in image
    mask = cv2.inRange(hsv, np.array([0, 60, 80]), np.array([20, 255, 255]))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f'Total orange contours: {len(contours)}')
    for i, cnt in enumerate(sorted(contours, key=cv2.contourArea, reverse=True)[:5]):
        area = cv2.contourArea(cnt)
        M = cv2.moments(cnt)
        if M['m00'] > 0:
            cu = int(M['m10']/M['m00'])
            cv_pos = int(M['m01']/M['m00'])
            print(f'  cont{i}: area={area:.0f} at ({cu},{cv_pos})')

print('\n=== HOME IMAGE (for comparison) ===')
fname = '/workspace/cal_test_home.jpg'
if os.path.exists(fname):
    img = cv2.imread(fname)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0, 60, 80]), np.array([20, 255, 255]))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f'Home image orange contours: {len(contours)}')
    for i, cnt in enumerate(sorted(contours, key=cv2.contourArea, reverse=True)[:5]):
        area = cv2.contourArea(cnt)
        M = cv2.moments(cnt)
        if M['m00'] > 0:
            cu = int(M['m10']/M['m00'])
            cv_pos = int(M['m01']/M['m00'])
            print(f'  cont{i}: area={area:.0f} at ({cu},{cv_pos})')
