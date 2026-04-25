#!/usr/bin/env python3
"""
Lightweight frontier explorer for AimeeNav + SLAM Toolbox.

Publishes /goal_pose in the odom frame.  When the robot is too close to
an obstacle, it clears the goal (publishes the robot's current position)
so AimeeNav falls back to pure reactive obstacle avoidance.
"""

import math
import time

import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
import tf2_ros
from tf2_ros import TransformException


class ExploreNode(Node):
    def __init__(self):
        super().__init__('explore_node')

        # Parameters
        self.declare_parameter('robot_frame', 'base_link')
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('odom_frame', 'odom')
        self.declare_parameter('goal_tolerance_m', 0.30)
        self.declare_parameter('frontier_min_dist_m', 0.50)
        self.declare_parameter('max_goal_dist_m', 1.20)
        self.declare_parameter('loop_period_s', 2.0)
        self.declare_parameter('goal_timeout_s', 30.0)
        self.declare_parameter('front_clear_m', 0.70)
        self.declare_parameter('front_blocked_m', 0.45)

        self._robot_frame = self.get_parameter('robot_frame').value
        self._map_frame = self.get_parameter('map_frame').value
        self._odom_frame = self.get_parameter('odom_frame').value
        self._goal_tol = self.get_parameter('goal_tolerance_m').value
        self._frontier_min_dist = self.get_parameter('frontier_min_dist_m').value
        self._max_goal_dist = self.get_parameter('max_goal_dist_m').value
        self._loop_period = self.get_parameter('loop_period_s').value
        self._goal_timeout = self.get_parameter('goal_timeout_s').value
        self._front_clear = self.get_parameter('front_clear_m').value
        self._front_blocked = self.get_parameter('front_blocked_m').value

        # Subscribers & Publishers
        self._map_sub = self.create_subscription(
            OccupancyGrid, '/map', self._on_map, 1
        )
        scan_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )
        self._scan_sub = self.create_subscription(
            LaserScan, '/scan', self._on_scan, scan_qos
        )
        self._goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 1)

        # TF
        self._tf_buffer = tf2_ros.Buffer()
        self._tf_listener = tf2_ros.TransformListener(self._tf_buffer, self)

        # State
        self._latest_map: OccupancyGrid | None = None
        self._front_dist = float('inf')
        self._current_goal = None
        self._goal_start_time = None
        self._exploration_done = False
        self._blocked = False

        # Timer
        self._timer = self.create_timer(self._loop_period, self._explore_loop)

        self.get_logger().info('ExploreNode started. Waiting for /map, /scan and TF...')

    def _on_map(self, msg: OccupancyGrid) -> None:
        self._latest_map = msg

    def _on_scan(self, msg: LaserScan) -> None:
        """Compute minimum distance in front sector (-30° to +30°)."""
        ranges = np.array(msg.ranges)
        angles = msg.angle_min + np.arange(len(ranges)) * msg.angle_increment
        # Normalize to [-180, 180]
        angles_deg = np.degrees(((angles + np.pi) % (2 * np.pi)) - np.pi)
        front_mask = (angles_deg >= -30.0) & (angles_deg <= 30.0)
        front_ranges = ranges[front_mask]
        valid = front_ranges[(front_ranges > msg.range_min) & (front_ranges < msg.range_max) & np.isfinite(front_ranges)]
        self._front_dist = float(valid.min()) if valid.size > 0 else float('inf')

    def _explore_loop(self) -> None:
        if self._exploration_done:
            return

        if self._latest_map is None:
            self.get_logger().warn('No map yet — waiting for SLAM...', throttle_duration_sec=5.0)
            return

        # Check if front is blocked
        if self._front_dist < self._front_blocked:
            if not self._blocked:
                self.get_logger().info(f'Front blocked ({self._front_dist:.2f} m) — clearing goal, letting reactive mode handle it')
                self._blocked = True
            self._clear_goal()
            return

        # Front must be clearly clear before resuming exploration
        if self._blocked and self._front_dist < self._front_clear:
            self.get_logger().info(f'Front still close ({self._front_dist:.2f} m) — waiting for clear path...')
            self._clear_goal()
            return

        if self._blocked:
            self.get_logger().info(f'Front clear ({self._front_dist:.2f} m) — resuming exploration')
            self._blocked = False

        # Get robot pose in map frame
        robot_x, robot_y = self._get_robot_pose(self._map_frame, self._robot_frame)
        if robot_x is None:
            self.get_logger().warn('Cannot get robot pose from TF', throttle_duration_sec=5.0)
            return

        # If we have an active goal, check if reached or timed out
        if self._current_goal is not None:
            rx, ry = self._get_robot_pose(self._odom_frame, self._robot_frame)
            if rx is None:
                return
            dx = rx - self._current_goal[0]
            dy = ry - self._current_goal[1]
            dist = math.hypot(dx, dy)
            elapsed = time.time() - self._goal_start_time

            if dist < self._goal_tol:
                self.get_logger().info(f'Goal reached ({dist:.2f} m)')
                self._current_goal = None
            elif elapsed > self._goal_timeout:
                self.get_logger().warn(f'Goal timeout ({elapsed:.1f} s) — picking new frontier')
                self._current_goal = None
            else:
                self.get_logger().debug(f'Pursuing goal: {dist:.2f} m remaining')
                return

        # Find frontiers in map frame
        frontiers = self._find_frontiers(self._latest_map)
        if not frontiers:
            self.get_logger().info('No frontiers found — exploration complete!')
            self._exploration_done = True
            return

        # Pick nearest frontier in map frame
        best_map = self._select_frontier(frontiers, robot_x, robot_y)
        if best_map is None:
            self.get_logger().warn('No valid frontier selected')
            return

        fmx, fmy = best_map
        f_dist = math.hypot(fmx - robot_x, fmy - robot_y)

        # If frontier is beyond local grid range, pick intermediate waypoint
        if f_dist > self._max_goal_dist:
            ratio = self._max_goal_dist / f_dist
            gmx = robot_x + (fmx - robot_x) * ratio
            gmy = robot_y + (fmy - robot_y) * ratio
            self.get_logger().info(
                f'Frontier at {f_dist:.2f}m — intermediate goal ({gmx:.2f},{gmy:.2f})'
            )
        else:
            gmx, gmy = fmx, fmy
            self.get_logger().info(f'Selected frontier ({gmx:.2f},{gmy:.2f}) dist={f_dist:.2f}m')

        # Transform goal from map frame to odom frame
        gox, goy = self._transform_point(gmx, gmy, self._map_frame, self._odom_frame)
        if gox is None:
            self.get_logger().warn('TF transform map→odom failed, skipping goal')
            return

        self._publish_goal(gox, goy, self._odom_frame)
        self._current_goal = (gox, goy)
        self._goal_start_time = time.time()

    # ------------------------------------------------------------------
    # Reactive safety: clear goal by publishing robot's current position
    # ------------------------------------------------------------------

    def _clear_goal(self) -> None:
        """Publish a goal at the robot's current position so AimeeNav drops it."""
        rx, ry = self._get_robot_pose(self._odom_frame, self._robot_frame)
        if rx is not None:
            self._publish_goal(rx, ry, self._odom_frame)
        self._current_goal = None

    # ------------------------------------------------------------------
    # Fast frontier detection (pure NumPy)
    # ------------------------------------------------------------------

    def _find_frontiers(self, msg: OccupancyGrid):
        width = msg.info.width
        height = msg.info.height
        resolution = msg.info.resolution
        origin_x = msg.info.origin.position.x
        origin_y = msg.info.origin.position.y

        data = np.array(msg.data, dtype=np.int8).reshape((height, width))
        free = data == 0
        unknown = data == -1

        un_n = np.roll(unknown, 1, axis=0);  un_n[0, :] = True
        un_s = np.roll(unknown, -1, axis=0); un_s[-1, :] = True
        un_e = np.roll(unknown, 1, axis=1);  un_e[:, 0] = True
        un_w = np.roll(unknown, -1, axis=1); un_w[:, -1] = True

        frontier_mask = free & (un_n | un_s | un_e | un_w)
        if not frontier_mask.any():
            return []

        rows, cols = np.where(frontier_mask)
        wx = origin_x + (cols + 0.5) * resolution
        wy = origin_y + (rows + 0.5) * resolution
        return list(zip(wx.tolist(), wy.tolist()))

    def _select_frontier(self, frontiers, robot_x, robot_y):
        best = None
        best_dist = float('inf')
        for fx, fy in frontiers:
            d = math.hypot(fx - robot_x, fy - robot_y)
            if d < self._frontier_min_dist:
                continue
            if d < best_dist:
                best_dist = d
                best = (fx, fy)
        return best

    # ------------------------------------------------------------------
    # TF helpers
    # ------------------------------------------------------------------

    def _get_robot_pose(self, target_frame, source_frame):
        try:
            t = self._tf_buffer.lookup_transform(
                target_frame, source_frame, rclpy.time.Time()
            )
            return t.transform.translation.x, t.transform.translation.y
        except TransformException as e:
            self.get_logger().debug(f'TF lookup {source_frame}->{target_frame} failed: {e}')
            return None, None

    def _transform_point(self, px, py, source_frame, target_frame):
        try:
            t = self._tf_buffer.lookup_transform(
                target_frame, source_frame, rclpy.time.Time()
            )
            tx = t.transform.translation.x
            ty = t.transform.translation.y
            qw = t.transform.rotation.w
            qz = t.transform.rotation.z
            cos_t = qw * qw - qz * qz
            sin_t = 2.0 * qw * qz
            px_rot = px * cos_t - py * sin_t
            py_rot = px * sin_t + py * cos_t
            return px_rot + tx, py_rot + ty
        except TransformException as e:
            self.get_logger().debug(f'TF transform failed: {e}')
            return None, None

    def _publish_goal(self, x, y, frame_id):
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = frame_id
        msg.pose.position.x = x
        msg.pose.position.y = y
        msg.pose.orientation.w = 1.0
        self._goal_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = ExploreNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
