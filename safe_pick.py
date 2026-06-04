#!/usr/bin/env python3
"""Single safe pick at calibrated position."""
import rclpy
from rclpy.node import Node
from aimee_msgs.msg import ArmCommand
import time

class SafePick(Node):
    def __init__(self):
        super().__init__('safe_pick')
        self.arm_pub = self.create_publisher(ArmCommand, '/arm/command', 10)
        time.sleep(1)
        
        # Calibrated from user measurement:
        # Z=-0.05 was 2.5cm above surface → surface at Z=-0.075
        # Pick at 1cm above surface → grasp_z = -0.065
        target_x = 0.31
        target_y = 0.0
        desk_z = -0.075
        grasp_z = desk_z + 0.01   # 1cm above surface
        safe_z = 0.05              # clears other items during transit
        lift_z = grasp_z + 0.08
        
        self.get_logger().info(f'Safe pick: X={target_x:.3f} Y={target_y:.3f} grasp_Z={grasp_z:.3f}')
        
        # 1. Home first
        self._send_home()
        time.sleep(6)
        
        # 2. Transit to target XY at safe height (faster: 4000ms)
        self._send_cartesian(target_x, target_y, safe_z, True, 4000)
        time.sleep(5)
        
        # 3. Lower to pick height (1cm above surface)
        self._send_cartesian(target_x, target_y, grasp_z, True, 3000)
        time.sleep(4)
        
        # 4. Close gripper
        self._send_cartesian(target_x, target_y, grasp_z, False, 2000)
        time.sleep(3)
        
        # 5. Lift to safe height
        self._send_cartesian(target_x, target_y, lift_z, False, 3000)
        time.sleep(4)
        
        # 6. Home
        self._send_home()
        time.sleep(5)
        
        self.get_logger().info('Pick sequence complete')
    
    def _send_cartesian(self, x, y, z, open_gripper, time_ms):
        cmd = ArmCommand()
        cmd.command_type = 'cartesian'
        cmd.target_pose.position.x = x
        cmd.target_pose.position.y = y
        cmd.target_pose.position.z = z
        cmd.target_pose.orientation.x = 0.0
        cmd.target_pose.orientation.y = 0.707
        cmd.target_pose.orientation.z = 0.0
        cmd.target_pose.orientation.w = 0.707
        cmd.gripper_position = 0.08 if open_gripper else 0.02
        cmd.cartesian_speed = float(time_ms)
        self.arm_pub.publish(cmd)
        g = "open" if open_gripper else "close"
        self.get_logger().info(f'Move: X={x:.3f} Y={y:.3f} Z={z:.3f} gripper={g} time={time_ms}ms')
    
    def _send_home(self):
        cmd = ArmCommand()
        cmd.command_type = 'home'
        self.arm_pub.publish(cmd)
        self.get_logger().info('Home')

def main():
    rclpy.init()
    node = SafePick()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
