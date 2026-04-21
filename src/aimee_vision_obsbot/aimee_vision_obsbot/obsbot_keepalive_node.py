#!/usr/bin/env python3
"""Lightweight keepalive node for OBSBOT Tiny 2 video stream.

The OBSBOT's USB audio interface only works when the UVC video interface
is actively streaming. This node opens the video device with v4l2-ctl
and discards frames, using <1% CPU.
"""

import logging
import subprocess
import sys

import rclpy
from rclpy.node import Node

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ObsbotKeepaliveNode(Node):
    def __init__(self):
        super().__init__('obsbot_keepalive')

        self.declare_parameter('device', '/dev/video2')
        self.declare_parameter('width', 160)
        self.declare_parameter('height', 120)
        self.declare_parameter('pixelformat', 'MJPG')

        device = self.get_parameter('device').value
        width = self.get_parameter('width').value
        height = self.get_parameter('height').value
        pixelformat = self.get_parameter('pixelformat').value

        self.get_logger().info(
            f"Starting OBSBOT keepalive for {device} ({width}x{height} {pixelformat})"
        )

        cmd = [
            'v4l2-ctl',
            '-d', device,
            '--set-fmt-video',
            f"width={width},height={height},pixelformat={pixelformat}",
            '--stream-mmap',
            '--stream-count=0',
            '--stream-to=/dev/null',
        ]

        self._proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        self.get_logger().info(f"v4l2-ctl started (pid {self._proc.pid})")

        # Create a timer to watchdog the process
        self._timer = self.create_timer(2.0, self._watchdog)

    def _watchdog(self):
        ret = self._proc.poll()
        if ret is not None:
            self.get_logger().error(f"v4l2-ctl exited with code {ret}; shutting down node")
            self._timer.cancel()
            raise SystemExit(1)

    def destroy_node(self):
        if self._proc and self._proc.poll() is None:
            self.get_logger().info("Stopping v4l2-ctl...")
            self._proc.terminate()
            try:
                self._proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._proc.kill()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = ObsbotKeepaliveNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
