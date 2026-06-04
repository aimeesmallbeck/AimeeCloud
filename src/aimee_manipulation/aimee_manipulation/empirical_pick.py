#!/usr/bin/env python3
"""
Empirical pick: detect pink character in camera image and pick using
calibrated image-to-arm coordinate mapping. All tunable parameters live
in /workspace/calibration.yaml for easy retuning when camera moves.

Usage inside container:
    ros2 run aimee_manipulation empirical_pick --ros-args --params-file /workspace/calibration.yaml
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose, Point, Quaternion
from aimee_msgs.msg import ArmCommand
import yaml
import numpy as np
import cv2
from cv_bridge import CvBridge
import time


class EmpiricalPick(Node):
    def __init__(self):
        super().__init__('empirical_pick')

        # Load calibration from YAML
        cal_path = self.declare_parameter('calibration_file', '/workspace/calibration.yaml').value
        try:
            with open(cal_path, 'r') as f:
                self.cal = yaml.safe_load(f)
            self.get_logger().info(f"Loaded calibration from {cal_path}")
        except Exception as e:
            self.get_logger().error(f"Failed to load {cal_path}: {e}")
            self.cal = {}

        # Calibration parameters
        self.cx = self.cal.get('image_center_x', 320.0)
        self.cy = self.cal.get('image_center_y', 240.0)
        self.scale_x = self.cal.get('scale_x', 0.0012)
        self.scale_y = self.cal.get('scale_y', -0.0010)
        self.offset_x = self.cal.get('offset_x', 0.10)
        self.offset_y = self.cal.get('offset_y', 0.0)
        self.skew_xy = self.cal.get('skew_xy', 0.0)
        self.skew_yx = self.cal.get('skew_yx', 0.0)
        # Empirically calibrated: Z=-0.05 was 2.5cm above surface → surface at Z=-0.075
        self.desk_z = self.cal.get('desk_z', -0.075)
        self.safe_z = self.cal.get('safe_z', 0.05)
        self.grasp_offset = self.cal.get('grasp_offset', 0.01)
        self.lift_height = self.cal.get('lift_height', 0.08)

        # HSV range for pink
        self.pink_hsv = {
            'h_min': self.cal.get('pink_hue_min', 165),
            'h_max': self.cal.get('pink_hue_max', 179),
            's_min': self.cal.get('pink_sat_min', 15),
            's_max': self.cal.get('pink_sat_max', 255),
            'v_min': self.cal.get('pink_val_min', 110),
            'v_max': self.cal.get('pink_val_max', 255),
        }
        self.min_area = self.cal.get('min_pink_area', 200)
        self.max_area = self.cal.get('max_pink_area', 20000)

        # State
        self._cv_bridge = CvBridge()
        self._latest_image = None
        self._latest_debug = None

        # Publishers
        self._arm_pub = self.create_publisher(ArmCommand, '/arm/command', 10)
        self._debug_pub = self.create_publisher(Image, '/vision/empirical_debug', 1)

        # Subscribers
        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=1)
        self._image_sub = self.create_subscription(
            Image, '/camera/color/image_raw', self._on_image, qos)

        # Timers
        self._debug_timer = self.create_timer(0.5, self._publish_debug)

        # CLI interface
        self.create_timer(1.0, self._print_status)

        self.get_logger().info(
            "EmpiricalPick ready.\n"
            "  Services: call /empirical_pick/do_pick (no args) to pick pink character\n"
            "  Call /empirical_pick/move_to_image (u,v) to test coordinate mapping"
        )

        # Services
        from std_srvs.srv import Trigger as TriggerSrv
        self._pick_srv = self.create_service(TriggerSrv, '/empirical_pick/do_pick', self._handle_pick)
        self._cal_srv = self.create_service(TriggerSrv, '/empirical_pick/do_calibration', self._handle_cal)

    def _on_image(self, msg: Image):
        try:
            self._latest_image = self._cv_bridge.imgmsg_to_cv2(msg, 'bgr8')
        except Exception as e:
            self.get_logger().debug(f"cv_bridge error: {e}")

    def _detect_pink(self, image: np.ndarray):
        """Detect pink character. Returns (u, v, area, debug_image) or (None, None, 0, debug_image)."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Handle wrap-around for pink (near 180/0 boundary)
        if self.pink_hsv['h_min'] > self.pink_hsv['h_max']:
            mask1 = cv2.inRange(hsv,
                                np.array([self.pink_hsv['h_min'], self.pink_hsv['s_min'], self.pink_hsv['v_min']]),
                                np.array([179, self.pink_hsv['s_max'], self.pink_hsv['v_max']]))
            mask2 = cv2.inRange(hsv,
                                np.array([0, self.pink_hsv['s_min'], self.pink_hsv['v_min']]),
                                np.array([self.pink_hsv['h_max'], self.pink_hsv['s_max'], self.pink_hsv['v_max']]))
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            mask = cv2.inRange(hsv,
                               np.array([self.pink_hsv['h_min'], self.pink_hsv['s_min'], self.pink_hsv['v_min']]),
                               np.array([self.pink_hsv['h_max'], self.pink_hsv['s_max'], self.pink_hsv['v_max']]))

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        debug = image.copy()
        cv2.putText(debug, f"Pink pixels: {cv2.countNonZero(mask)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        best = None
        best_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if self.min_area <= area <= self.max_area and area > best_area:
                best_area = area
                best = cnt

        if best is not None:
            # Use bottom of contour as pick point (accounts for camera angle / parallax)
            max_v = np.max(best[:, 0, 1])
            bottom_pixels = best[np.abs(best[:, 0, 1] - max_v) <= 3]
            u = int(np.median(bottom_pixels[:, 0, 0]))
            v = int(max_v)
            
            # Also compute centroid for debug display
            M = cv2.moments(best)
            if M['m00'] > 0:
                cu = int(M['m10'] / M['m00'])
                cv = int(M['m01'] / M['m00'])
                cv2.circle(debug, (cu, cv), 3, (255, 0, 0), -1)  # centroid in blue
            
            cv2.circle(debug, (u, v), 5, (0, 255, 0), -1)
            cv2.drawContours(debug, [best], -1, (0, 255, 0), 2)
            cv2.putText(debug, f"Pick ({u},{v}) A={int(best_area)}", (u+10, v),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            return u, v, best_area, debug

        return None, None, 0, debug

    def image_to_arm(self, u: int, v: int) -> tuple[float, float]:
        """Map image pixel (u,v) to arm base frame (X,Y) using calibrated affine transform."""
        du = u - self.cx
        dv = self.cy - v  # positive when v is above center (forward)

        arm_x = self.scale_x * dv + self.skew_xy * du + self.offset_x
        arm_y = self.scale_y * du + self.skew_yx * dv + self.offset_y
        return arm_x, arm_y

    def _send_cartesian(self, x: float, y: float, z: float, gripper_open: bool, time_ms: int = 4000):
        cmd = ArmCommand()
        cmd.command_type = 'cartesian'
        cmd.target_pose.position.x = x
        cmd.target_pose.position.y = y
        cmd.target_pose.position.z = z
        cmd.target_pose.orientation.x = 0.0
        cmd.target_pose.orientation.y = 0.707
        cmd.target_pose.orientation.z = 0.0
        cmd.target_pose.orientation.w = 0.707
        cmd.gripper_position = 0.08 if gripper_open else 0.02
        cmd.cartesian_speed = float(time_ms)
        self._arm_pub.publish(cmd)
        self.get_logger().info(f"Arm cmd: X={x:.3f} Y={y:.3f} Z={z:.3f} gripper={'open' if gripper_open else 'close'}")

    def _send_home(self):
        cmd = ArmCommand()
        cmd.command_type = ArmCommand.HOME
        self._arm_pub.publish(cmd)
        self.get_logger().info("Arm cmd: HOME")

    def run_pick_sequence(self, target_x: float, target_y: float):
        """Execute safe pick at target (X,Y) with desk Z from calibration."""
        grasp_z = self.desk_z + self.grasp_offset  # pick slightly above surface
        lift_z = grasp_z + self.lift_height

        # 1. Transit to target XY at safe height
        self._send_cartesian(target_x, target_y, self.safe_z, True, 6000)
        time.sleep(7)

        # 2. Lower to grasp height (1cm above surface)
        self._send_cartesian(target_x, target_y, grasp_z, True, 4000)
        time.sleep(5)

        # 3. Close gripper
        self._send_cartesian(target_x, target_y, grasp_z, False, 3000)
        time.sleep(4)

        # 4. Lift to safe height
        self._send_cartesian(target_x, target_y, lift_z, False, 4000)
        time.sleep(5)

        # 5. Home
        self._send_home()
        time.sleep(6)

    def _handle_pick(self, request, response):
        """Service callback: detect pink and pick."""
        if self._latest_image is None:
            self.get_logger().error("No image available")
            response.success = False
            response.message = "No image available"
            return response

        u, v, area, debug = self._detect_pink(self._latest_image)
        self._latest_debug = debug

        if u is None:
            self.get_logger().error("Pink character not detected")
            response.success = False
            response.message = "Pink character not detected"
            return response

        arm_x, arm_y = self.image_to_arm(u, v)
        self.get_logger().info(
            f"Detected pink at image=({u},{v}) area={area:.0f} -> "
            f"arm=({arm_x:.3f}, {arm_y:.3f})"
        )

        self.run_pick_sequence(arm_x, arm_y)

        response.success = True
        response.message = f"Picked at ({arm_x:.3f}, {arm_y:.3f})"
        return response

    def _handle_cal(self, request, response):
        """Service callback: run calibration sequence (fwd sweep at Y=0)."""
        self.get_logger().info("Starting calibration sweep: X=[0.10, 0.35] step 0.05, Y=0")
        for x in np.arange(0.10, 0.36, 0.05):
            self.get_logger().info(f"Calibration move to X={x:.2f}, Y=0.00")
            self._send_cartesian(x, 0.0, self.safe_z, True, 4000)
            time.sleep(5)
            self._send_cartesian(x, 0.0, self.desk_z, True, 3000)
            time.sleep(5)
        self._send_home()
        response.success = True
        response.message = "Calibration sweep complete"
        return response

    def _publish_debug(self):
        if self._latest_image is not None:
            _, _, _, debug = self._detect_pink(self._latest_image)
            self._latest_debug = debug
        if self._latest_debug is not None:
            try:
                msg = self._cv_bridge.cv2_to_imgmsg(self._latest_debug, 'bgr8')
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = 'camera_color_frame'
                self._debug_pub.publish(msg)
            except Exception as e:
                self.get_logger().debug(f"Debug publish error: {e}")

    def _print_status(self):
        if self._latest_image is not None:
            u, v, area, _ = self._detect_pink(self._latest_image)
            if u is not None:
                ax, ay = self.image_to_arm(u, v)
                self.get_logger().info(f"Pink at img=({u},{v}) -> arm=({ax:.3f},{ay:.3f})")


def main(args=None):
    rclpy.init(args=args)
    node = EmpiricalPick()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
