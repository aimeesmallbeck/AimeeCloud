#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from aimee_msgs.msg import ObjectDetection
import socket
import msgpack
import time
import numpy as np

# Known physical position of the arm in the 'floor test' pose (meters)
# Relative to arm_base_link
ROBOT_X = 0.196
ROBOT_Y = 0.000
ROBOT_Z = -0.088
ROBOT_PITCH = 1.57 # Straight down

class AutoCalibrator(Node):
    def __init__(self):
        super().__init__('auto_calibrator')
        self.subscription = self.create_subscription(
            ObjectDetection,
            '/vision/detections_3d',
            self.detection_callback,
            10
        )
        self.detections = []
        self.required_samples = 10
        self.is_calibrating = False

    def send_arm_to_calibration_pose(self):
        print("\n--- Moving Arm to Calibration Position ---")
        print(f"Target: X={ROBOT_X}, Y={ROBOT_Y}, Z={ROBOT_Z}, Pitch={ROBOT_PITCH}")
        
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.connect('/var/run/arduino-router.sock')
            # First go home safely
            print("Moving to Home...")
            home_raw = [2056, 2060, 2636, 2484, 2043, 2062]
            sock.sendall(msgpack.packb([2, "receive_waypoints", home_raw + [3000]]))
            time.sleep(4.0)
            
            # Then to calibration pose
            print("Moving to Calibration Pose...")
            gripper = 0.08 # Open
            sock.sendall(msgpack.packb([2, "receive_cartesian", [ROBOT_X, ROBOT_Y, ROBOT_Z, ROBOT_PITCH, gripper, 3000]]))
            time.sleep(4.0)
            print("Arm is in position.")
        except Exception as e:
            print(f"Failed to move arm: {e}")
        finally:
            sock.close()

    def detection_callback(self, msg):
        if not self.is_calibrating:
            return
            
        if msg.color.lower() != "yellow":
            return
            
        # We only care about the camera's raw optical frame data
        # Ignore msg.position_robot, we are trying to fix the TF that generates it!
        cam_x = msg.position_camera.x
        cam_y = msg.position_camera.y
        cam_z = msg.position_camera.z
        
        # Ensure it has depth data
        if cam_z == 0:
            return
            
        self.detections.append([cam_x, cam_y, cam_z])
        print(f"Captured sample {len(self.detections)}/{self.required_samples}: x={cam_x:.3f}, y={cam_y:.3f}, z={cam_z:.3f}")
        
        if len(self.detections) >= self.required_samples:
            self.is_calibrating = False
            self.calculate_transform()

    def calculate_transform(self):
        # Average the optical frame coordinates to reduce noise
        avg_cam = np.mean(self.detections, axis=0)
        c_x, c_y, c_z = avg_cam[0], avg_cam[1], avg_cam[2]
        
        print("\n--- Calibration Results ---")
        print(f"Known Robot Target: X={ROBOT_X:.3f}, Y={ROBOT_Y:.3f}, Z={ROBOT_Z:.3f}")
        print(f"Optical Camera Avg: X={c_x:.3f}, Y={c_y:.3f}, Z={c_z:.3f}")
        
        # Calculate Translation Offsets
        # In ROS standard:
        # Optical Frame: X=Right, Y=Down, Z=Forward
        # Base Frame: X=Forward, Y=Left, Z=Up
        #
        # Mapping:
        # Robot_X = Camera_Z + Transform_X  =>  Transform_X = Robot_X - Camera_Z
        # Robot_Y = -Camera_X + Transform_Y =>  Transform_Y = Robot_Y + Camera_X
        # Robot_Z = -Camera_Y + Transform_Z =>  Transform_Z = Robot_Z + Camera_Y
        
        t_x = ROBOT_X - c_z
        t_y = ROBOT_Y + c_x
        t_z = ROBOT_Z + c_y
        
        print("\n=== UPDATED TF ARGUMENTS ===")
        print("Please update /home/arduino/aimee-robot-ws/src/aimee_bringup/launch/vision_pipeline.launch.py")
        print("Under the 'camera_to_arm_tf' node, replace the arguments with:")
        print(f"'{t_x:.4f}', '{t_y:.4f}', '{t_z:.4f}', # Translation X, Y, Z (meters)")
        print("'0.0', '0.0', '0.0', # Rotation Yaw, Pitch, Roll (radians)")
        print("============================\n")
        
        # Return arm to home
        print("Returning arm to Home...")
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.connect('/var/run/arduino-router.sock')
            home_raw = [2056, 2060, 2636, 2484, 2043, 2062]
            sock.sendall(msgpack.packb([2, "receive_waypoints", home_raw + [3000]]))
            time.sleep(3.5)
        except:
            pass
        finally:
            sock.close()
            
        print("Done. Press Ctrl+C to exit.")

def main(args=None):
    rclpy.init(args=args)
    node = AutoCalibrator()
    
    print("\nStarting Camera-to-Arm Auto Calibration")
    node.send_arm_to_calibration_pose()
    
    print("\nAction Required: Please place a GREEN BLOCK directly inside the closed gripper jaws.")
    print("You have 20 seconds to place the block before visual sampling begins...")
    time.sleep(20)
    
    print("\nStarting visual sampling...")
    node.is_calibrating = True
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
