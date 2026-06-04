#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from aimee_msgs.msg import GraspPose
from geometry_msgs.msg import Pose
import math
import time
import socket
import msgpack

# RPC Message Types
REQUEST = 0
RESPONSE = 1
NOTIFY = 2

class ArmKinematicsBridgeRPC(Node):
    def __init__(self):
        super().__init__('arm_kinematics_bridge_rpc')
        
        self.declare_parameter('router_socket', '/var/run/arduino-router.sock')
        sock_path = self.get_parameter('router_socket').value
        
        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.sock.connect(sock_path)
            self.get_logger().info(f"Connected to STM32 RPC via Router at {sock_path}")
        except Exception as e:
            self.get_logger().error(f"Failed to connect to router socket: {e}")
            self.sock = None
            
        self.subscription = self.create_subscription(
            GraspPose,
            '/manipulation/grasp_pose',
            self.grasp_pose_callback,
            10
        )
        self.get_logger().info("Arm Kinematics Bridge (RPC) initialized with Real IK Solver.")

    def rpc_notify(self, method, *args):
        if not self.sock:
            self.get_logger().error("Cannot send RPC: Socket not connected")
            return
            
        request = [NOTIFY, method, [*args]]
        packed = msgpack.packb(request)
        try:
            self.sock.sendall(packed)
            self.get_logger().info(f"RPC Notify sent: {method}({args})")
        except Exception as e:
            self.get_logger().error(f"Failed to send RPC: {e}")

    def calculate_ik(self, pose: Pose, gripper_width: float):
        """
        Real 2D Inverse Kinematics for RoArm-M3 Parallel Linkage.
        Compensates for UGV02 base height using physical calibration data.
        """
        x = pose.position.x
        y = pose.position.y
        z = pose.position.z

        # --- UGV02 & Hardware Safety Bounds ---
        # From physical calibration, wrist Z at table floor is exactly 0.088m
        SAFE_WRIST_Z_MIN = 0.088
        if z < SAFE_WRIST_Z_MIN:
            self.get_logger().warn(f"SAFETY: Wrist Z={z:.3f} below UGV02 floor limit! Clipping to {SAFE_WRIST_Z_MIN}")
            z = SAFE_WRIST_Z_MIN
            
        r = math.sqrt(x**2 + y**2)
        MIN_REACH = 0.10
        if r < MIN_REACH:
            self.get_logger().warn(f"SAFETY: Reach {r:.3f} too close to base. Clipping to {MIN_REACH}")
            scale = MIN_REACH / r if r > 0 else MIN_REACH
            x *= scale
            y *= scale
            r = MIN_REACH

        # --- Real 2D Inverse Kinematics ---
        L1 = 0.1215  # Base to Shoulder Z (meters)
        L2 = 0.2368  # Shoulder to Elbow (meters)
        L3 = 0.2803  # Elbow to Wrist (meters)
        
        r_target = r
        z_target = z - L1
        
        D = math.sqrt(r_target**2 + z_target**2)
        max_reach = L2 + L3 - 0.001
        if D > max_reach:
            self.get_logger().warn(f"IK: Target out of reach ({D:.3f}m). Clipping to max ({max_reach:.3f}m).")
            scale = max_reach / D
            r_target *= scale
            z_target *= scale
            D = max_reach
            
        # Law of Cosines for inner angle alpha
        cos_alpha = (L2**2 + D**2 - L3**2) / (2 * L2 * D)
        cos_alpha = max(-1.0, min(1.0, cos_alpha))
        alpha = math.acos(cos_alpha)
        
        # Angle of target from shoulder
        theta_target = math.atan2(z_target, r_target)
        
        # Elbow-up configuration (L2 is higher)
        theta_2 = theta_target + alpha
        
        # Calculate Elbow (L3) absolute angle
        r_elbow = L2 * math.cos(theta_2)
        z_elbow = L2 * math.sin(theta_2)
        r_L3 = r_target - r_elbow
        z_L3 = z_target - z_elbow
        theta_3 = math.atan2(z_L3, r_L3)
        
        # --- Map to Raw Encoders (Parallel Linkage) ---
        yaw = math.atan2(y, x)
        raw_base = int(2047 + (yaw * 4096 / (2 * math.pi)))
        raw_base = max(1023, min(3071, raw_base)) # +/- 90 deg swing
        
        # Shoulder: 2047 is UP. Forward pitches increase raw value.
        raw_shoulder = int(2047 - (theta_2 - math.pi/2) * 4096 / (2 * math.pi))
        raw_shoulder = max(2047, min(4095, raw_shoulder)) # Prevent bending backwards
        
        # Elbow: 2047 is DOWN. Forward pitches decrease raw value.
        raw_elbow = int(2047 - (theta_3 + math.pi/2) * 4096 / (2 * math.pi))
        raw_elbow = max(0, min(4095, raw_elbow))
        
        # Wrist Pitch from Quaternion
        q = pose.orientation
        sinp = 2 * (q.w * q.y - q.z * q.x)
        pitch = math.asin(max(-1.0, min(1.0, sinp)))
        # If pointing straight down (pitch=pi/2), wrist should be 2047.
        raw_wrist = int(2047 + ((math.pi/2 - pitch) * 4096 / (2 * math.pi)))
        raw_wrist = max(0, min(4095, raw_wrist))
        
        # Gripper (0.0m = 2061, 0.08m = 853)
        w_clamped = max(0.0, min(0.08, gripper_width))
        if w_clamped <= 0.005: raw_gripper = 2061
        elif w_clamped >= 0.075: raw_gripper = 853
        else: raw_gripper = int(2061 - (w_clamped * 15100))
        
        return [raw_base, raw_shoulder, raw_elbow, raw_wrist, 2047, raw_gripper]

    def grasp_pose_callback(self, msg: GraspPose):
        self.get_logger().info(f"Executing sequence for object: {msg.object_id}")
        home_pose = Pose()
        home_pose.position.x = 0.2
        home_pose.position.y = 0.0
        home_pose.position.z = 0.3
        
        wp_home = self.calculate_ik(home_pose, msg.gripper_open_width)
        self.rpc_notify("receive_waypoints", *wp_home, 2000)
        time.sleep(2.0)
        
        wp_approach = self.calculate_ik(msg.pre_grasp_pose, msg.gripper_open_width)
        self.rpc_notify("receive_waypoints", *wp_approach, 1500)
        time.sleep(1.5)
        
        wp_grasp = self.calculate_ik(msg.grasp_pose, msg.gripper_close_width)
        self.rpc_notify("receive_waypoints", *wp_grasp, 1000)
        time.sleep(1.0)
        
        wp_retract = self.calculate_ik(msg.lift_pose, msg.gripper_close_width)
        self.rpc_notify("receive_waypoints", *wp_retract, 1500)
        time.sleep(1.5)
        
        wp_drop = self.calculate_ik(home_pose, msg.gripper_open_width)
        self.rpc_notify("receive_waypoints", *wp_drop, 2000)
        time.sleep(2.0)
        
        self.get_logger().info("Sequence complete.")

def main(args=None):
    rclpy.init(args=args)
    node = ArmKinematicsBridgeRPC()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
