import numpy as np
import math

L1 = 0.12606
L2 = 0.23871
t2rad = 0.1259
L3 = 0.14449
t3rad = 0.0
LE = 0.17221
tErad = 0.0795

def raw_to_rad(raw, offset=2047, mult=1.0):
    return (raw - offset) * math.pi / 2048.0 * mult

def fk(s_raw, e_raw, w_raw):
    s_rad = raw_to_rad(s_raw, 2047, 1.0)
    e_rad = raw_to_rad(e_raw, 1024, 1.0)
    w_rad = raw_to_rad(w_raw, 2047, 1.0)

    l1 = 0.12606
    l2 = 0.23871
    t2rad = 0.1259
    l3 = 0.14449
    lE = 0.17221
    tErad = 0.0795

    angle2 = math.pi/2 - (s_rad + t2rad)
    aOut = l2 * math.cos(angle2)
    bOut = l2 * math.sin(angle2)

    angle3 = math.pi/2 - (e_rad + s_rad)
    cOut = l3 * math.cos(angle3)
    dOut = l3 * math.sin(angle3)

    angleE = math.pi/2 - (e_rad + s_rad + w_rad + tErad)
    eOut = lE * math.cos(angleE)
    fOut = lE * math.sin(angleE)

    r_ee = aOut + cOut + eOut
    z_ee = bOut + dOut + fOut
    return r_ee, z_ee

def fk_full(joints):
    j1, j2, j3, j4 = joints[0], joints[1], joints[3], joints[4]
    yaw = (2047 - j1) * math.pi / 2048.0
    r_ee, z_ee = fk(j2, j3, j4)
    x = r_ee * math.cos(yaw)
    y = r_ee * math.sin(yaw)
    z = z_ee + 0.12606
    return x, y, z

points = [
    # (u, v), raw_joints
    ((45, 391), [1479,2723,1400,2133,2313,2045,1111]),
    ((158, 207), [1874,2919,1201,1445,2784,2045,1111]),
    ((361, 218), [2230,2922,1194,1445,2785,2046,1111]),
    ((428, 341), [2467,2743,1381,2021,2419,2042,1112]),
]

image_center_x = 320.0
image_center_y = 240.0

A = []
B_x = []
B_y = []

for (u, v), joints in points:
    arm_x, arm_y, arm_z = fk_full(joints)
    print(f"Point ({u}, {v}) -> arm_X={arm_x:.4f}, arm_Y={arm_y:.4f}, arm_Z={arm_z:.4f}")
    du = u - image_center_x
    dv = image_center_y - v
    # x = scale_x * dv + skew_xy * du + offset_x
    A.append([dv, du, 1])
    B_x.append(arm_x)
    # y = scale_y * du + skew_yx * dv + offset_y
    B_y.append(arm_y)

A = np.array(A)
B_x = np.array(B_x)
B_y = np.array(B_y)

# Fit X params
x_params, _, _, _ = np.linalg.lstsq(A, B_x, rcond=None)
scale_x, skew_xy, offset_x = x_params

# Fit Y params
# Note: y = scale_y * du + skew_yx * dv + offset_y
# So for Y, the row is [du, dv, 1]
A_y = []
for (u, v), joints in points:
    du = u - image_center_x
    dv = image_center_y - v
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
for i, ((u, v), _) in enumerate(points):
    du = u - image_center_x
    dv = image_center_y - v
    pred_x = scale_x * dv + skew_xy * du + offset_x
    pred_y = scale_y * du + skew_yx * dv + offset_y
    err_x = pred_x - B_x[i]
    err_y = pred_y - B_y[i]
    err_dist = math.hypot(err_x, err_y)
    print(f"Pt {i+1}: dx={err_x*1000:+.1f}mm, dy={err_y*1000:+.1f}mm, dist={err_dist*1000:.1f}mm")
