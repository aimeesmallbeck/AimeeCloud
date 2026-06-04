#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from aimee_msgs.msg import GraspPose, ArmCommand
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
        
        self.cmd_subscription = self.create_subscription(
            ArmCommand,
            '/arm/command',
            self.arm_command_callback,
            10
        )
        
        self.get_logger().info("Arm Kinematics Bridge (RPC) initialized with Precise IK Solver.")

    def rpc_notify(self, method, *args):
        if not self.sock:
            self.get_logger().error("Cannot send RPC: Socket not connected")
            return
            
        request = [NOTIFY, method, [*args]]
        packed = msgpack.packb(request)
        try:
            self.sock.sendall(packed)
        except Exception as e:
            self.get_logger().error(f"Failed to send RPC: {e}")

    def calculate_ik(self, pose: Pose, gripper_width: float):
        """
        Real 2D Inverse Kinematics matching the exact Waveshare ESP32 firmware logic.
        """
        x = pose.position.x
        y = pose.position.y
        z = pose.position.z

        # Link lengths in meters
        L1 = 0.12606
        L2 = 0.23871
        t2rad = 0.1259
        L3 = 0.14449
        t3rad = 0.0
        LE = 0.17221
        tErad = 0.0795

        # Base angle and target radius
        r_target = math.sqrt(x**2 + y**2)
        yaw = math.atan2(y, x)

        # 1. Wrist offset
        # Determine pitch from quaternion
        q = pose.orientation
        sinp = 2 * (q.w * q.y - q.z * q.x)
        pitch = math.asin(max(-1.0, min(1.0, sinp)))
        
        # In Waveshare FK, pitch = angle of end effector relative to ground
        angleE = pitch
        r_wrist = r_target - LE * math.cos(angleE)
        z_wrist = z - L1 - LE * math.sin(angleE)

        LA = L2
        LB = L3

        aIn = r_wrist
        bIn = z_wrist

        L2C = aIn*aIn + bIn*bIn
        LC = math.sqrt(L2C)
        
        if LC > (LA + LB):
            self.get_logger().warn(f"IK: Target out of reach ({LC:.3f}m > max {LA+LB:.3f}m).")
            # Scale down the wrist target to max reach
            scale = (LA + LB - 0.001) / LC
            aIn *= scale
            bIn *= scale
            L2C = aIn*aIn + bIn*bIn
            LC = math.sqrt(L2C)

        # Calculate IK inner angles
        lambda_ang = math.atan2(bIn, aIn)
        cos_psi = (LA*LA + L2C - LB*LB) / (2 * LA * LC)
        cos_psi = max(-1.0, min(1.0, cos_psi))
        psi = math.acos(cos_psi) + t2rad

        alpha = math.pi / 2.0 - lambda_ang - psi

        cos_omega = (LB*LB + L2C - LA*LA) / (2 * LC * LB)
        cos_omega = max(-1.0, min(1.0, cos_omega))
        omega = math.acos(cos_omega)

        beta = psi + omega - t3rad

        # Calculate required wrist angle to maintain pitch
        w_rad = math.pi/2 - angleE - beta - alpha - tErad

        # Convert to raw encoder values (0-4095)
        raw_base = int(2047 + (yaw * 2048 / math.pi))
        raw_base = max(1023, min(3071, raw_base))
        
        raw_shoulder = int(2047 + alpha * 2048 / math.pi)
        raw_shoulder = max(2047, min(4095, raw_shoulder))
        
        raw_elbow = int(2047 + beta * 2048 / math.pi)
        raw_elbow = max(0, min(4095, raw_elbow))
        
        raw_wrist = int(2047 + w_rad * 2048 / math.pi)
        raw_wrist = max(0, min(4095, raw_wrist))

        # Gripper Mapping
        w_clamped = max(0.0, min(0.08, gripper_width))
        if w_clamped <= 0.005: raw_gripper = 2061
        elif w_clamped >= 0.075: raw_gripper = 853
        else: raw_gripper = int(2061 - (w_clamped * 15100))
        
        return [raw_base, raw_shoulder, raw_elbow, raw_wrist, 2047, raw_gripper]

    def arm_command_callback(self, msg: ArmCommand):
        if msg.command_type == "raw_joints":
            if len(msg.joint_angles) >= 6:
                joints = [int(j) for j in msg.joint_angles[:6]]
                time_ms = int(msg.joint_speed) if msg.joint_speed > 0 else 1500
                self.rpc_notify("receive_waypoints", *joints, time_ms)
                self.get_logger().info(f"Direct Command - Raw Joints: {joints}")
                
        elif msg.command_type == "cartesian":
            gripper_w = msg.gripper_position if msg.gripper_position > 0 else 0.08
            joints = self.calculate_ik(msg.target_pose, gripper_w)
            time_ms = int(msg.cartesian_speed) if msg.cartesian_speed > 0 else 1500
            self.rpc_notify("receive_waypoints", *joints, time_ms)
            self.get_logger().info(f"Direct Command - Cartesian Pose: X={msg.target_pose.position.x:.2f} Z={msg.target_pose.position.z:.2f} -> Joints: {joints}")
            
        elif msg.command_type == "home":
            home_pose = Pose()
            home_pose.position.x = 0.321
            home_pose.position.z = 0.432
            # To get pitch 0.670 (from home calibration):
            # sin(pitch) = 0.620, so q.y = 0.31... Let's just use Euler
            cy = math.cos(0)
            sy = math.sin(0)
            cp = math.cos(0.670 * 0.5)
            sp = math.sin(0.670 * 0.5)
            cr = math.cos(0)
            sr = math.sin(0)
            home_pose.orientation.w = cr * cp * cy + sr * sp * sy
            home_pose.orientation.y = cr * sp * cy + sr * cp * sy
            joints = self.calculate_ik(home_pose, 0.08)
            self.rpc_notify("receive_waypoints", *joints, 2000)
            self.get_logger().info(f"Direct Command - Home Sequence")

    def grasp_pose_callback(self, msg: GraspPose):
        self.get_logger().info(f"Executing grasp sequence for object: {msg.object_id}")
        
        home_pose = Pose()
        home_pose.position.x = 0.321
        home_pose.position.z = 0.432
        cy = math.cos(0); sy = math.sin(0); cr = math.cos(0); sr = math.sin(0)
        cp = math.cos(0.670 * 0.5); sp = math.sin(0.670 * 0.5)
        home_pose.orientation.w = cr * cp * cy + sr * sp * sy
        home_pose.orientation.y = cr * sp * cy + sr * cp * sy
        
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
