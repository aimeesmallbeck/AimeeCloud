#!/usr/bin/env python3
import numpy as np
import cv2
import json

def main():
    print("=== Calculating Affine Transform ===")
    
    # 1. Pixel Coordinates (u, v) from our ground truth session
    # Source points (Image coordinates)
    # 4A: (76, 433)
    # 4H: (604, 437)
    # 8A: (41, 137)
    # 8H: (618, 123)
    src_pts = np.array([
        [76, 433],
        [604, 437],
        [41, 137],
        [618, 123]
    ], dtype=np.float32)

    # 2. Physical Coordinates (x, y) 
    # Based on the user's grid definition, we established these as the physical bounds
    # Note: These values were from the initial assumed map in self_learn_grid.py.
    # 4A = (0.18, 0.12)
    # 4H = (0.18, -0.12)
    # 8A = (0.32, 0.12)
    # 8H = (0.32, -0.12)
    dst_pts = np.array([
        [0.18, 0.12],
        [0.18, -0.12],
        [0.32, 0.12],
        [0.32, -0.12]
    ], dtype=np.float32)

    # Calculate Perspective Transform (more accurate than affine for camera angles)
    # Even looking straight down, perspective transform handles slight pitch/roll errors better.
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    
    print("\nTransform Matrix (M):")
    print(M)
    
    # Save to file
    config = {
        "look_x": 0.300,
        "look_y": 0.000,
        "look_z": 0.200,
        "pitch": 1.571,
        "transform_matrix": M.tolist()
    }
    
    with open('vision_calibration.json', 'w') as f:
        json.dump(config, f, indent=4)
        
    print("\nSaved configuration to vision_calibration.json")
    
    # Verify the mapping by re-calculating the points
    print("\n--- Verification ---")
    for i, pt in enumerate(src_pts):
        # Add a 1 for the perspective division
        pt_3d = np.array([pt[0], pt[1], 1.0])
        mapped = np.dot(M, pt_3d)
        mapped_x = mapped[0] / mapped[2]
        mapped_y = mapped[1] / mapped[2]
        
        target = dst_pts[i]
        err_x = mapped_x - target[0]
        err_y = mapped_y - target[1]
        
        print(f"Pixel ({pt[0]:.0f}, {pt[1]:.0f}) -> physical ({mapped_x:.4f}, {mapped_y:.4f})")
        print(f"  Target: ({target[0]:.4f}, {target[1]:.4f}) | Error: X={err_x*1000:.1f}mm, Y={err_y*1000:.1f}mm")

if __name__ == '__main__':
    main()
