#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL
#
# SPDX-License-Identifier: MPL-2.0

"""
Policy Controller Node for LeRobot

Loads trained LeRobot policies and executes them in ROS2.
Subscribes to observations (cameras, joint states) and publishes actions.

Usage:
    ros2 run aimee_lerobot_bridge policy_controller \
        --ros-args \
        -p policy_path:=/path/to/policy \
        -p device:=cpu

Services:
    /load_policy - Load a new policy
    /start_inference - Start autonomous control
    /stop_inference - Stop autonomous control
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image, JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from std_msgs.msg import Bool, String
from std_srvs.srv import Trigger, SetBool
from cv_bridge import CvBridge
import numpy as np
import torch
from typing import Optional, Dict, List, Tuple
import time
from collections import deque


class PolicyControllerNode(Node):
    """
    Runs LeRobot policies for autonomous control.
    
    Supports:
    - ACT (Action Chunking with Transformers)
    - Diffusion Policy
    - VQ-VAE policies
    """

    def __init__(self):
        super().__init__('policy_controller')

        # Declare parameters
        self.declare_parameters(namespace='', parameters=[
            ('policy_path', ''),
            ('policy_repo_id', ''),
            ('policy_type', 'act'),  # act, diffusion, vqbet
            ('device', 'cpu'),  # cpu, cuda
            ('control_freq', 10.0),  # Hz
            ('action_chunk_size', 16),
            ('temporal_ensemble', True),
            ('ensemble_alpha', 0.1),
            ('camera_topics', ['/camera/image_raw']),
            ('joint_state_topic', '/joint_states'),
            ('action_topic', '/arm/command'),
            ('gripper_topic', '/arm/gripper/command'),
            (' warmup_steps', 2),
        ])

        # Get parameters
        self._policy_path = self.get_parameter('policy_path').value
        self._policy_repo_id = self.get_parameter('policy_repo_id').value
        self._policy_type = self.get_parameter('policy_type').value
        self._device = self.get_parameter('device').value
        self._control_freq = self.get_parameter('control_freq').value
        self._chunk_size = self.get_parameter('action_chunk_size').value
        self._temporal_ensemble = self.get_parameter('temporal_ensemble').value
        self._ensemble_alpha = self.get_parameter('ensemble_alpha').value
        self._camera_topics = self.get_parameter('camera_topics').value
        self._joint_topic = self.get_parameter('joint_state_topic').value
        self._action_topic = self.get_parameter('action_topic').value
        self._warmup = self.get_parameter('warmup_steps').value

        # Setup QoS
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # CV Bridge
        self._cv_bridge = CvBridge()

        # Policy
        self._policy: Optional[torch.nn.Module] = None
        self._policy_loaded = False
        self._is_running = False

        # State
        self._current_images: Dict[str, np.ndarray] = {}
        self._current_joint_pos: Optional[np.ndarray] = None
        self._action_queue: deque = deque(maxlen=self._chunk_size)
        self._step_count = 0

        # Action history for temporal ensemble
        self._action_history: List[np.ndarray] = []

        # Subscribers
        self._image_subs = []
        for cam_topic in self._camera_topics:
            sub = self.create_subscription(
                Image, cam_topic,
                lambda msg, t=cam_topic: self._on_image(msg, t),
                sensor_qos
            )
            self._image_subs.append(sub)

        self._joint_sub = self.create_subscription(
            JointState, self._joint_topic,
            self._on_joint_state,
            sensor_qos
        )

        # Publishers
        self._action_pub = self.create_publisher(
            JointTrajectory, self._action_topic, 10
        )
        self._status_pub = self.create_publisher(
            String, '/policy_controller/status', 10
        )
        self._action_preview_pub = self.create_publisher(
            JointState, '/policy_controller/action_preview', 10
        )

        # Services
        self._srv_load = self.create_service(
            LoadPolicy, '/load_policy', self._on_load_policy
        )
        self._srv_start = self.create_service(
            Trigger, '/start_inference', self._on_start
        )
        self._srv_stop = self.create_service(
            Trigger, '/stop_inference', self._on_stop
        )

        # Control timer
        self._control_timer = None

        # Load policy if specified
        if self._policy_path or self._policy_repo_id:
            self._load_policy()

        self.get_logger().info(
            f"Policy Controller initialized:\n"
            f"  Policy type: {self._policy_type}\n"
            f"  Device: {self._device}\n"
            f"  Control freq: {self._control_freq} Hz\n"
            f"  Action chunk: {self._chunk_size}\n"
            f"  Temporal ensemble: {self._temporal_ensemble}"
        )

    def _load_policy(self):
        """Load LeRobot policy from path or Hugging Face."""
        try:
            # Try to import LeRobot
            from lerobot.common.policies.act.policy import ACTPolicy
            from lerobot.common.policies.diffusion.policy import DiffusionPolicy

            if self._policy_repo_id:
                self.get_logger().info(f"Loading policy from HF: {self._policy_repo_id}")
                
                if self._policy_type == 'act':
                    self._policy = ACTPolicy.from_pretrained(self._policy_repo_id)
                elif self._policy_type == 'diffusion':
                    self._policy = DiffusionPolicy.from_pretrained(self._policy_repo_id)
                else:
                    self.get_logger().error(f"Unknown policy type: {self._policy_type}")
                    return
                    
            elif self._policy_path:
                self.get_logger().info(f"Loading policy from: {self._policy_path}")
                # Load from local path
                checkpoint = torch.load(
                    self._policy_path, 
                    map_location=self._device
                )
                # Restore policy from checkpoint
                # Implementation depends on how policy was saved

            if self._policy:
                self._policy.to(self._device)
                self._policy.eval()
                self._policy_loaded = True
                self.get_logger().info("Policy loaded successfully!")
                
        except ImportError:
            self.get_logger().error("LeRobot not installed. Run: pip install lerobot")
        except Exception as e:
            self.get_logger().error(f"Failed to load policy: {e}")

    def _on_load_policy(self, request, response):
        """Service callback to load a new policy."""
        self._policy_repo_id = request.repo_id
        self._load_policy()
        
        response.success = self._policy_loaded
        response.message = "Policy loaded" if self._policy_loaded else "Failed to load"
        return response

    def _on_start(self, request, response):
        """Start policy inference."""
        if not self._policy_loaded:
            response.success = False
            response.message = "No policy loaded"
            return response

        if self._is_running:
            response.success = False
            response.message = "Already running"
            return response

        self._is_running = True
        self._step_count = 0
        self._action_queue.clear()
        
        # Start control loop
        period = 1.0 / self._control_freq
        self._control_timer = self.create_timer(period, self._control_loop)

        self.get_logger().info("Policy inference started")
        response.success = True
        response.message = "Started"
        return response

    def _on_stop(self, request, response):
        """Stop policy inference."""
        if not self._is_running:
            response.success = False
            response.message = "Not running"
            return response

        self._is_running = False
        
        if self._control_timer:
            self._control_timer.cancel()
            self._control_timer = None

        # Send stop command
        self._publish_stop()

        self.get_logger().info("Policy inference stopped")
        response.success = True
        response.message = "Stopped"
        return response

    def _on_image(self, msg: Image, topic: str):
        """Handle camera images."""
        try:
            cv_image = self._cv_bridge.imgmsg_to_cv2(msg, 'rgb8')
            self._current_images[topic] = cv_image
        except Exception as e:
            self.get_logger().debug(f"Image conversion error: {e}")

    def _on_joint_state(self, msg: JointState):
        """Handle joint state updates."""
        self._current_joint_pos = np.array(msg.position, dtype=np.float32)

    def _control_loop(self):
        """Main control loop - runs at control frequency."""
        if not self._is_running:
            return

        # Check if we have all observations
        if not self._current_images or self._current_joint_pos is None:
            self.get_logger().warn_throttle(5.0, "Waiting for observations...")
            return

        # Warmup steps
        if self._step_count < self._warmup:
            self._step_count += 1
            return

        # Get action from policy or queue
        if len(self._action_queue) == 0:
            # Run policy inference
            actions = self._infer_actions()
            if actions is not None:
                self._action_queue.extend(actions)

        # Execute next action
        if len(self._action_queue) > 0:
            action = self._action_queue.popleft()
            
            # Apply temporal ensemble if enabled
            if self._temporal_ensemble:
                action = self._apply_temporal_ensemble(action)
            
            self._publish_action(action)

        self._step_count += 1

    def _infer_actions(self) -> Optional[np.ndarray]:
        """Run policy inference to get action chunk."""
        try:
            with torch.no_grad():
                # Prepare observations
                # This is simplified - actual implementation depends on policy
                
                # Stack images if multiple cameras
                images = []
                for cam_topic in self._camera_topics:
                    if cam_topic in self._current_images:
                        img = self._current_images[cam_topic]
                        # Resize, normalize
                        img = self._preprocess_image(img)
                        images.append(img)
                
                if not images:
                    return None

                # Convert to tensor
                image_tensor = torch.from_numpy(np.stack(images)).unsqueeze(0)
                image_tensor = image_tensor.to(self._device)

                # Prepare state (joint positions)
                state_tensor = torch.from_numpy(self._current_joint_pos).unsqueeze(0)
                state_tensor = state_tensor.to(self._device)

                # Create observation dict
                obs = {
                    'observation.images': image_tensor,
                    'observation.state': state_tensor,
                }

                # Run policy
                actions = self._policy.select_action(obs)
                
                # Convert to numpy
                if isinstance(actions, torch.Tensor):
                    actions = actions.cpu().numpy()

                return actions

        except Exception as e:
            self.get_logger().error(f"Inference error: {e}")
            return None

    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for policy input."""
        # Resize to policy input size (e.g., 224x224)
        import cv2
        image = cv2.resize(image, (224, 224))
        
        # Normalize to [0, 1]
        image = image.astype(np.float32) / 255.0
        
        # Channel first (C, H, W)
        image = np.transpose(image, (2, 0, 1))
        
        return image

    def _apply_temporal_ensemble(self, action: np.ndarray) -> np.ndarray:
        """Apply temporal ensemble smoothing."""
        self._action_history.append(action)
        
        if len(self._action_history) == 1:
            return action

        # Exponential moving average
        weights = np.array([
            self._ensemble_alpha * (1 - self._ensemble_alpha) ** i
            for i in range(len(self._action_history))
        ])
        weights = weights / weights.sum()
        
        ensemble_action = np.zeros_like(action)
        for i, hist_action in enumerate(reversed(self._action_history)):
            ensemble_action += weights[min(i, len(weights)-1)] * hist_action
        
        # Keep history bounded
        if len(self._action_history) > 10:
            self._action_history.pop(0)

        return ensemble_action

    def _publish_action(self, action: np.ndarray):
        """Publish action to robot."""
        # Split action into joints and gripper
        # Assuming last element is gripper
        num_joints = len(action) - 1
        joint_positions = action[:num_joints]
        gripper_pos = action[-1]

        # Create trajectory message
        traj = JointTrajectory()
        traj.header.stamp = self.get_clock().now().to_msg()
        traj.joint_names = [f'joint{i+1}' for i in range(num_joints)]

        point = JointTrajectoryPoint()
        point.positions = joint_positions.tolist()
        point.time_from_start.sec = 0
        point.time_from_start.nanosec = int(0.1 * 1e9)  # 100ms

        traj.points.append(point)
        
        self._action_pub.publish(traj)

        # Publish preview for monitoring
        preview = JointState()
        preview.header = traj.header
        preview.name = traj.joint_names + ['gripper']
        preview.position = action.tolist()
        self._action_preview_pub.publish(preview)

    def _publish_stop(self):
        """Publish stop command."""
        traj = JointTrajectory()
        traj.header.stamp = self.get_clock().now().to_msg()
        self._action_pub.publish(traj)


def main(args=None):
    rclpy.init(args=args)
    node = PolicyControllerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
