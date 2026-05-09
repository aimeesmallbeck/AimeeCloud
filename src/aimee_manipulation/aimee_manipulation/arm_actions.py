#!/usr/bin/env python3
import math
import time

class ArmActions:
    """
    Library for predefined Aimee arm sequences.
    
    MOTION DEFINITIONS (Joint mapping for RoArm-M3):
    - Base (J1): +deg = Right (Clockwise), -deg = Left (Counter-Clockwise)
    - Shoulder (J2): +deg = Forward/Down, -deg = Back/Up (Vertical = 0)
    - Elbow (J3): +deg = Down/Fold, -deg = Up/Extend
    - Wrist (J4): +deg = Down/Forward, -deg = Up/Back
    - Roll (J5): +deg = Counter-Clockwise (from front), -deg = Clockwise
    - Gripper (J6): Width in meters (0.0 = closed, 0.08 = open)
    """
    
    # Common Named Poses
    POSES = {
        "HOME": [2056, 2060, 2636, 2484, 2043, 2062],
        "FOLDED": [2048, 2048, 4095, 2048, 2048, 2062],
        "FLOOR_READY": [2056, 2060, 1024, 2048, 2043, 2062]
    }
    
    # Calibrated Home (Raw Encoder Values)
    HOME_RAW = POSES["HOME"]
    
    # Conversion constants
    STEPS_PER_RAD = 2048.0 / math.pi
    
    @staticmethod
    def deg_to_raw(deg, center=2048, inverted=False):
        rad = math.radians(deg)
        offset = int(rad * ArmActions.STEPS_PER_RAD)
        return center - offset if inverted else center + offset

    def get_wave_sequence(self):
        """
        Sequence:
        1. Base: 80 deg Right
        2. Shoulder: 5 deg down from vertical
        3. Elbow: 45 deg raised
        4. Roll: 90 deg rotation (side-wave pose)
        5. Wrist: Wave back and forth twice (120 deg range) around a HIGHER center
        """
        
        # 1. Setup Pose (Ready to wave)
        # Base: 80 deg Right. 
        base_target = self.deg_to_raw(-80, center=2056) 
        
        # Shoulder: 5 deg down from vertical. 
        shoulder_target = self.deg_to_raw(5, center=2060)
        
        # Elbow: 45 deg raised. 
        elbow_target = self.deg_to_raw(-45, center=2048)
        
        # Roll: 90 deg rotation. 
        roll_target = self.deg_to_raw(90, center=2043)
        
        # HIGHER Wrist Center: -20 deg (20 deg UP from straight)
        wrist_center_deg = -20
        wrist_center = self.deg_to_raw(wrist_center_deg, center=2048)
        
        # Gripper: Stay at Home (approx 2062)
        gripper = 2062
        
        setup_pose = [base_target, shoulder_target, elbow_target, wrist_center, roll_target, gripper]
        
        # 2. Wave Motion (Wrist Only)
        wave_1 = setup_pose.copy()
        wave_1[3] = self.deg_to_raw(wrist_center_deg - 60, center=2048)
        
        wave_2 = setup_pose.copy()
        wave_2[3] = self.deg_to_raw(wrist_center_deg + 60, center=2048)
        
        return {
            "setup": setup_pose,
            "wave_points": [wave_1, wave_2, wave_1, wave_2],
            "home": self.HOME_RAW
        }

    def get_figure_8_stream(self, duration_sec=8.0):
        """
        Generates a high-resolution 50Hz figure-8 stream using a 
        True Lemniscate of Bernoulli for a rounded "infinity" look.
        """
        center_x = 0.30
        center_z = 0.212
        pitch = 0.0
        gripper = 0.0 # CLOSED
        
        # 'a' is the distance from the center to the focus/vertex.
        # This will create a path approx 40cm wide and 15-20cm tall.
        a = 0.20 
        
        points = []
        num_points = int(duration_sec * 50)
        
        for i in range(num_points):
            t = (i / float(num_points)) * 2 * math.pi
            
            # Lemniscate of Bernoulli parametric equations:
            # x = a * cos(t) / (1 + sin(t)^2)
            # y = a * sin(t) * cos(t) / (1 + sin(t)^2)
            
            denom = 1 + math.sin(t)**2
            # We map Lemniscate-X to our World-Y (Width)
            # and Lemniscate-Y to our World-Z (Height)
            y_val = (a * math.cos(t)) / denom
            z_off = (a * math.sin(t) * math.cos(t)) / denom
            
            points.append([center_x, y_val, center_z + z_off, pitch, gripper])
            
        return {
            "center": [center_x, 0.0, center_z, pitch, gripper],
            "points": points,
            "home": self.HOME_RAW
        }
