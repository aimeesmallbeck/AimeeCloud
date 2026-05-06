#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from aimee_msgs.msg import GraspPose
from geometry_msgs.msg import Pose
import math
import time
import socket
import msgpack

# RPC Message Types (from Arduino_RPClite)
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
        self.get_logger().info("Arm Kinematics Bridge (RPC) initialized. Listening on /manipulation/grasp_pose")

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
        # --- HARDWARE SAFETY INTERLOCKS ---
        # 1. Z-Axis Floor (Prevent smashing table)
        SAFE_Z_MIN = 0.08  # Minimum wrist height (8cm protects down-pointing gripper)
        if pose.position.z < SAFE_Z_MIN:
            self.get_logger().warn(f"SAFETY INTERLOCK: Z={pose.position.z:.3f} below floor! Clipping to {SAFE_Z_MIN}")
            pose.position.z = SAFE_Z_MIN
            
        # 2. Radial Reach Limits (Prevent overextension/crashing into base)
        MAX_REACH = 0.35  # Max reach in meters
        MIN_REACH = 0.10  # Min distance from base
        distance = math.sqrt(pose.position.x**2 + pose.position.y**2)
        
        if distance > MAX_REACH:
            self.get_logger().warn(f"SAFETY INTERLOCK: Reach {distance:.3f} exceeds max {MAX_REACH}! Clipping.")
            scale = MAX_REACH / distance
            pose.position.x *= scale
            pose.position.y *= scale
            distance = MAX_REACH
        elif distance < MIN_REACH:
            self.get_logger().warn(f"SAFETY INTERLOCK: Reach {distance:.3f} too close to base! Clipping.")
            scale = MIN_REACH / distance if distance > 0 else MIN_REACH
            if distance > 0:
                pose.position.x *= scale
                pose.position.y *= scale
            else:
                pose.position.x = MIN_REACH
            distance = MIN_REACH

        # --- IK CALCULATION ---
        joints = [2047] * 6
        yaw = math.atan2(pose.position.y, pose.position.x)
        joints[0] = int(2047 + (yaw * 2048.0 / math.pi))
        joints[1] = int(2047 + ((distance - 0.2) * 1000))
        joints[2] = int(2047 - ((pose.position.z - 0.1) * 1000))
        joints[3] = 2047
        joints[4] = 2047
        joints[5] = int(2047 + (gripper_width * 10000))
        return [max(0, min(4095, j)) for j in joints]

    def grasp_pose_callback(self, msg: GraspPose):
        self.get_logger().info(f"Received GraspPose for object: {msg.object_id}")
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
        
        self.get_logger().info("RPC Maneuver sequence complete.")

def main(args=None):
    rclpy.init(args=args)
    node = ArmKinematicsBridgeRPC()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
