#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
OBSBOT Vision Brick - PTZ Camera Control using official SDK

Uses the OBSBOT SDK (libdev.so) for control via UVC/USB.
Supports: Tiny 2, Tiny 2 Lite, Tiny SE, and other OBSBOT cameras.
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Callable, Dict, Any, List

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None

# Import SDK wrapper
try:
    from .obsbot_sdk_helper import (
        ObsbotSDKHelper, ObsbotDeviceHelper,
        AiWorkMode, AiSubMode, DevStatus
    )
    SDK_AVAILABLE = True
except ImportError as e:
    print(f"SDK import error: {e}")
    SDK_AVAILABLE = False
    # Fallback definitions
    class AiWorkMode(Enum):
        None_ = 0
        Group = 1
        Human = 2
        Hand = 3
        WhiteBoard = 4
        Desk = 5
    
    class AiSubMode(Enum):
        Normal = 0
        UpperBody = 1
        CloseUp = 2
        HeadHide = 3
        LowerBody = 4

# Import Arduino brick decorator
try:
    from arduino.app_utils import brick
except ImportError:
    def brick(cls):
        return cls

logger = logging.getLogger(__name__)


class TrackingMode(Enum):
    """OBSBOT AI Tracking Modes."""
    OFF = -1
    NORMAL = 0          # Person tracking (default)
    UPPER_BODY = 1
    CLOSEUP = 2
    HEADLESS = 3        # Below head tracking
    DESK = 4            # Desk mode (30° down)
    WHITEBOARD = 5
    HAND = 6
    GROUP = 7


@dataclass
class ObsbotStatus:
    """Current OBSBOT camera status."""
    connected: bool = False
    tracking_mode: TrackingMode = TrackingMode.OFF
    zoom_level: int = 0              # 0-100 (0=1x, 50=2x, 100=4x)
    pan_position: float = 0.0        # Degrees
    tilt_position: float = 0.0       # Degrees
    is_sleeping: bool = False
    battery_level: Optional[int] = None
    error_message: Optional[str] = None


@dataclass
class FaceDetection:
    """Face detection result."""
    x: float
    y: float
    width: float
    height: float
    confidence: float
    face_id: Optional[str] = None


@brick
class ObsbotBrick:
    """
    OBSBOT Camera Control Brick using official SDK.
    
    Provides full PTZ control, AI tracking, and preset management
    for OBSBOT Tiny 2, Tiny 2 Lite, and compatible cameras.
    """
    
    def __init__(
        self,
        sdk_path: str = "/workspace/libdev_v2.1.0_8/linux/arm64-release/libdev.so",
        camera_index: int = 0,
        auto_reconnect: bool = True,
        tracking_sensitivity: float = 0.5,
        debug: bool = False
    ):
        self.sdk_path = sdk_path
        self.camera_index = camera_index
        self.auto_reconnect = auto_reconnect
        self.tracking_sensitivity = tracking_sensitivity
        self.debug = debug
        
        # SDK instance
        self._sdk: Optional[ObsbotSDKHelper] = None
        self._device: Optional[ObsbotDeviceHelper] = None
        
        # Video capture (optional)
        self._cap: Optional[Any] = None
        
        # State
        self._status = ObsbotStatus()
        self._running = False
        self._initialized = False
        self._device_connected = False
        
        # Tracking
        self._face_position: Optional[tuple] = None
        self._auto_track_face = False
        self._tracking_task: Optional[asyncio.Task] = None
        
        # Callbacks
        self._callbacks: Dict[str, List[Callable]] = {
            'status_change': [],
            'face_detected': [],
            'tracking_update': [],
            'error': []
        }
        
        if debug:
            logging.basicConfig(level=logging.DEBUG)
    
    async def initialize(self) -> 'ObsbotBrick':
        """Initialize the brick and connect to camera."""
        logger.info("Initializing OBSBOT brick...")
        
        if not SDK_AVAILABLE:
            logger.error("SDK wrapper not available")
            self._status.error_message = "SDK not available"
            return self
        
        # Initialize SDK
        self._sdk = ObsbotSDKHelper()
        if not self._sdk.initialize():
            logger.warning("SDK initialization failed, will retry")
            if self.auto_reconnect:
                asyncio.create_task(self._reconnect_loop())
        else:
            logger.info("SDK initialized successfully")
            
            # Wait for device detection (SDK detects async via helper)
            logger.info("Waiting for device detection...")
            await asyncio.sleep(3)  # Give SDK time to detect
            
            # Check for devices (with retry)
            count = self._sdk.get_device_count()
            logger.info(f"SDK reports {count} device(s)")
            
            # Check if Tiny 2 Lite is connected
            if self._sdk.is_tiny2_lite_connected():
                logger.info("Tiny 2 Lite detected via USB!")
                
                # Wait a bit more for full initialization
                await asyncio.sleep(1)
                
                # Try to get first device
                self._device = self._sdk.get_first_device()
                if self._device:
                    logger.info(f"Got device handle: {self._device}")
                    self._device_connected = True
                    self._status.connected = True
                else:
                    logger.warning("Could not get device handle, will retry")
                    asyncio.create_task(self._wait_for_device())
            else:
                devices = self._sdk.scan_devices()
                if devices:
                    logger.info(f"Found {len(devices)} OBSBOT device(s)")
                    self._device_connected = True
                    self._status.connected = True
        
        self._initialized = True
        self._running = True
        
        # Start status monitoring
        asyncio.create_task(self._status_monitor())
        
        return self
    
    async def _wait_for_device(self):
        """Wait for device to be ready and get handle."""
        retries = 10
        while not self._device_connected and retries > 0 and self._running:
            await asyncio.sleep(1)
            retries -= 1
            
            if self._sdk:
                count = self._sdk.get_device_count()
                if count > 0:
                    logger.info(f"Device count now: {count}, getting handle...")
                    self._device = self._sdk.get_first_device()
                    if self._device:
                        self._device_connected = True
                        self._status.connected = True
                        logger.info("✓ Camera connected and ready!")
                        self._trigger_callbacks('status_change', self._status)
                        return
        
        if not self._device_connected:
            logger.warning("Could not connect to camera after retries")
    
    async def _reconnect_loop(self):
        """Background reconnection task."""
        while not self._device_connected and self._running:
            await asyncio.sleep(3)
            
            if self._sdk and self._sdk.is_tiny2_lite_connected():
                self._device = self._sdk.get_first_device()
                if self._device:
                    self._device_connected = True
                    self._status.connected = True
                    logger.info("Camera connected!")
                    self._trigger_callbacks('status_change', self._status)
    
    async def _status_monitor(self):
        """Monitor camera status."""
        while self._running:
            try:
                if self._sdk and self._device_connected:
                    # Could poll status here if SDK supports it
                    pass
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"Status monitor error: {e}")
    
    # === PTZ Control ===
    
    def gimbal_up(self, speed: int = 50) -> bool:
        """Move gimbal up. Speed: 0-100."""
        if not self._device_connected or not self._device:
            logger.warning("No device connected")
            return False
        
        speed = max(0, min(100, speed))
        result = self._device.set_gimbal_speed(0, speed, 0)
        logger.info(f"Gimbal UP: speed={speed}, result={result}")
        return result
    
    def gimbal_down(self, speed: int = 50) -> bool:
        """Move gimbal down. Speed: 0-100."""
        if not self._device_connected or not self._device:
            logger.warning("No device connected")
            return False
        
        speed = max(0, min(100, speed))
        result = self._device.set_gimbal_speed(0, -speed, 0)
        logger.info(f"Gimbal DOWN: speed={speed}, result={result}")
        return result
    
    def gimbal_left(self, speed: int = 50) -> bool:
        """Move gimbal left. Speed: 0-100."""
        if not self._device_connected or not self._device:
            logger.warning("No device connected")
            return False
        
        speed = max(0, min(100, speed))
        result = self._device.set_gimbal_speed(-speed, 0, 0)
        logger.info(f"Gimbal LEFT: speed={speed}, result={result}")
        return result
    
    def gimbal_right(self, speed: int = 50) -> bool:
        """Move gimbal right. Speed: 0-100."""
        if not self._device_connected or not self._device:
            logger.warning("No device connected")
            return False
        
        speed = max(0, min(100, speed))
        result = self._device.set_gimbal_speed(speed, 0, 0)
        logger.info(f"Gimbal RIGHT: speed={speed}, result={result}")
        return result
    
    def stop_gimbal(self) -> bool:
        """Stop gimbal movement."""
        if not self._device_connected or not self._device:
            return False
        result = self._device.stop_gimbal()
        logger.info(f"Gimbal STOP: {result}")
        return result
    
    def set_zoom(self, level: int) -> bool:
        """
        Set zoom level.
        level: 0-100 (0=1x, 50=2x, 100=4x)
        """
        if not self._device_connected or not self._device:
            return False
        
        level = max(0, min(100, level))
        self._status.zoom_level = level
        
        # Convert 0-100 to 1.0-4.0
        zoom_value = 1.0 + (level / 100.0) * 3.0
        result = self._device.set_zoom_absolute(zoom_value)
        logger.info(f"Zoom: {level}% ({zoom_value}x), result={result}")
        return result
    
    def zoom_in(self, step: int = 10) -> bool:
        """Zoom in by step amount."""
        return self.set_zoom(self._status.zoom_level + step)
    
    def zoom_out(self, step: int = 10) -> bool:
        """Zoom out by step amount."""
        return self.set_zoom(self._status.zoom_level - step)
    
    # === AI Tracking ===
    
    def set_tracking_mode(self, mode: TrackingMode) -> bool:
        """Set AI tracking mode."""
        if not self._device_connected or not self._device:
            logger.warning("No device connected for tracking")
            return False
        
        self._status.tracking_mode = mode
        
        # Map our TrackingMode to SDK AiWorkMode
        mode_map = {
            TrackingMode.OFF: AiWorkMode.None_,
            TrackingMode.NORMAL: AiWorkMode.Human,
            TrackingMode.UPPER_BODY: AiWorkMode.Human,
            TrackingMode.CLOSEUP: AiWorkMode.Human,
            TrackingMode.HEADLESS: AiWorkMode.Human,
            TrackingMode.DESK: AiWorkMode.Desk,
            TrackingMode.WHITEBOARD: AiWorkMode.WhiteBoard,
            TrackingMode.HAND: AiWorkMode.Hand,
            TrackingMode.GROUP: AiWorkMode.Group,
        }
        
        sdk_mode = mode_map.get(mode, AiWorkMode.Human)
        
        # Set sub-mode for human tracking
        sub_mode = AiSubMode.Normal
        if mode == TrackingMode.UPPER_BODY:
            sub_mode = AiSubMode.UpperBody
        elif mode == TrackingMode.CLOSEUP:
            sub_mode = AiSubMode.CloseUp
        elif mode == TrackingMode.HEADLESS:
            sub_mode = AiSubMode.HeadHide
        
        result = self._device.set_ai_mode(sdk_mode, sub_mode)
        self._trigger_callbacks('tracking_update', mode)
        logger.info(f"Tracking mode set: {mode.name}, result={result}")
        return result
    
    def enable_tracking(self, mode: TrackingMode = TrackingMode.NORMAL) -> bool:
        """Enable AI tracking."""
        return self.set_tracking_mode(mode)
    
    def disable_tracking(self) -> bool:
        """Disable AI tracking."""
        return self.set_tracking_mode(TrackingMode.OFF)
    
    def track_face(self, face_position: tuple) -> bool:
        """Auto-adjust gimbal to track face position."""
        if not self._device_connected:
            return False
        
        x, y = face_position
        x_offset = x - 0.5
        y_offset = y - 0.5
        
        deadzone = 0.1
        speed_scale = 100 * self.tracking_sensitivity
        
        moved = False
        
        if abs(x_offset) > deadzone and self._device:
            speed = int(abs(x_offset) * speed_scale)
            if x_offset > 0:
                self._device.set_gimbal_speed(speed, 0, 0)
            else:
                self._device.set_gimbal_speed(-speed, 0, 0)
            moved = True
        
        if abs(y_offset) > deadzone and self._device:
            speed = int(abs(y_offset) * speed_scale)
            if y_offset > 0:
                self._device.set_gimbal_speed(0, speed, 0)
            else:
                self._device.set_gimbal_speed(0, -speed, 0)
            moved = True
        
        return moved
    
    # === Presets ===
    
    def save_preset(self, position_id: int) -> bool:
        """Save current position as preset (0-9)."""
        if not self._device_connected or not self._device:
            return False
        
        position_id = max(0, min(9, position_id))
        # TODO: Implement preset save
        logger.info(f"Save preset {position_id} - TODO")
        return True
    
    def recall_preset(self, position_id: int) -> bool:
        """Recall saved preset position."""
        if not self._device_connected or not self._device:
            return False
        
        position_id = max(0, min(9, position_id))
        # TODO: Implement preset recall
        logger.info(f"Recall preset {position_id} - TODO")
        return True
    
    # === Power Management ===
    
    def sleep(self) -> bool:
        """Put camera to sleep."""
        if not self._device_connected or not self._device:
            return False
        result = self._device.sleep()
        if result:
            self._status.is_sleeping = True
        return result
    
    def wake_up(self) -> bool:
        """Wake camera from sleep."""
        if not self._device_connected or not self._device:
            return False
        result = self._device.wake_up()
        if result:
            self._status.is_sleeping = False
        return result
    
    # === Video Capture ===
    
    async def get_frame(self) -> Optional[Any]:
        """Get current video frame."""
        if CV2_AVAILABLE and self._cap and self._cap.isOpened():
            ret, frame = self._cap.read()
            if ret:
                return frame
        return None
    
    # === Callbacks ===
    
    def on_status_change(self, callback: Callable[[ObsbotStatus], None]):
        """Register status change callback."""
        self._callbacks['status_change'].append(callback)
    
    def on_face_detected(self, callback: Callable[[FaceDetection], None]):
        """Register face detection callback."""
        self._callbacks['face_detected'].append(callback)
    
    def on_tracking_update(self, callback: Callable[[TrackingMode], None]):
        """Register tracking update callback."""
        self._callbacks['tracking_update'].append(callback)
    
    def on_error(self, callback: Callable[[str], None]):
        """Register error callback."""
        self._callbacks['error'].append(callback)
    
    def _trigger_callbacks(self, event: str, data: Any):
        """Trigger registered callbacks."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    # === Status & Info ===
    
    def get_status(self) -> ObsbotStatus:
        """Get current camera status."""
        return self._status
    
    def is_connected(self) -> bool:
        """Check if camera is connected."""
        return self._device_connected
    
    # === Lifecycle ===
    
    async def shutdown(self):
        """Clean shutdown."""
        logger.info("Shutting down OBSBOT brick...")
        self._running = False
        
        if self._tracking_task:
            self._tracking_task.cancel()
        
        if self._cap:
            self._cap.release()
            self._cap = None
        
        if self._sdk:
            self._sdk.shutdown()
            self._sdk = None
        
        self._device = None
        self._device_connected = False
        self._status.connected = False
        
        logger.info("OBSBOT brick shutdown complete")
