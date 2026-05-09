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
            
        # BUG FIX: Removed rogue subscription to /manipulation/grasp_pose that was 
        # causing autonomous and un-validated movement.
        
        self.cmd_subscription = self.create_subscription(
            ArmCommand,
            '/arm/command',
            self.arm_command_callback,
            10
        )
        
        self.get_logger().info("Arm Kinematics Bridge (RPC) initialized. STM32 acts as Hardware Abstraction Layer.")
        
        # Enforce Safe Home Position on Startup
        self.get_logger().info("Sending initial SAFE HOME command to STM32 to clear any invalid states...")
        self.rpc_notify("receive_waypoints", 2056, 2060, 2636, 2484, 2043, 2062, 5000)

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

    def send_cartesian(self, pose, gripper_w, time_ms):
        q = pose.orientation
        sinp = 2 * (q.w * q.y - q.z * q.x)
        pitch = math.asin(max(-1.0, min(1.0, sinp)))
        self.rpc_notify("receive_cartesian", pose.position.x, pose.position.y, pose.position.z, pitch, gripper_w, time_ms)

    def arm_command_callback(self, msg: ArmCommand):
        """Directly accept pose or raw joint commands from the PickPlace Server."""
        if msg.command_type == "raw_joints":
            if len(msg.joint_angles) >= 6:
                joints = [int(j) for j in msg.joint_angles[:6]]
                time_ms = int(msg.joint_speed) if msg.joint_speed > 0 else 5000
                self.rpc_notify("receive_waypoints", *joints, time_ms)
                self.get_logger().info(f"Direct Command - Raw Joints: {joints}")
                
        elif msg.command_type == "cartesian":
            gripper_w = msg.gripper_position if msg.gripper_position > 0 else 0.08
            time_ms = int(msg.cartesian_speed) if msg.cartesian_speed > 0 else 5000
            self.send_cartesian(msg.target_pose, gripper_w, time_ms)
            self.get_logger().info(f"Direct Command - Cartesian Pose: X={msg.target_pose.position.x:.2f} Z={msg.target_pose.position.z:.2f}")
            
        elif msg.command_type == "home":
            time_ms = 5000
            # Send home using the direct raw waypoints so we know it's 100% mechanically safe
            self.rpc_notify("receive_waypoints", 2056, 2060, 2636, 2484, 2043, 2062, time_ms)
            self.get_logger().info(f"Direct Command - Home Sequence sent to STM32")
            
        elif msg.command_type == "grasp":
            # Safely commanded by the pick_place_server, NOT autonomously.
            grasp = msg.grasp_pose
            self.get_logger().info(f"Executing PickPlace Grasp Sequence...")
            # 1. Approach
            self.send_cartesian(grasp.pre_grasp_pose, grasp.gripper_open_width, 1500)
            time.sleep(1.5)
            # 2. Grasp
            self.send_cartesian(grasp.grasp_pose, grasp.gripper_close_width, 1000)
            
        elif msg.command_type == "gripper":
            # Adjust gripper without moving arm
            gripper_w = msg.gripper_position if msg.gripper_position > 0 else 0.08
            # Fetch current physical state to hold arm still
            # For safety, if we don't have current state, we shouldn't send 0.0.0.0
            # For now, pick_place_server uses Cartesian to open/close when placing.
            self.get_logger().info(f"Gripper only command received: {gripper_w}")

def main(args=None):
    rclpy.init(args=args)
    node = ArmKinematicsBridgeRPC()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
