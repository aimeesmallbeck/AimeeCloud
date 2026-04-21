#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

"""
OBSBOT Vision Brick - PTZ Camera Control using official SDK

Optimized Version: UVC Video capture has been stripped out to conserve CPU.
This script strictly handles SDK communication (PTZ, AI Tracking, Status).
Video streaming should be handled by a dedicated C++ ROS2 node (e.g., v4l2_camera).
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Callable, Dict, Any, List

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


@brick
class ObsbotBrick:
    """
    OBSBOT Camera Control Brick using official SDK.
    
    Provides full PTZ control, AI tracking, and preset management.
    Note: Video capture is offloaded for efficiency.
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
        
        # State
        self._status = ObsbotStatus()
        self._running = False
        self._initialized = False
        self._device_connected = False
        
        # Tracking Task
        self._tracking_task: Optional[asyncio.Task] = None
        
        # Callbacks
        self._callbacks: Dict[str, List[Callable]] = {
            'status_change': [],
            'tracking_update': [],
            'error': []
        }
        
        if debug:
            logging.basicConfig(level=logging.DEBUG)
    
    async def initialize(self) -> 'ObsbotBrick':
        """Initialize the brick and connect to camera via SDK."""
        logger.info("Initializing OBSBOT SDK controller...")
        
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
            
            logger.info("Waiting for device detection...")
            await asyncio.sleep(3)  
            
            count = self._sdk.get_device_count()
            logger.info(f"SDK reports {count} device(s)")
            
            if self._sdk.is_tiny2_lite_connected():
                logger.info("Tiny 2 Lite detected via USB!")
                await asyncio.sleep(1)
                
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
                        logger.info("Camera connected and ready!")
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
                    pass  # Poll status here if SDK supports it
                await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"Status monitor error: {e}")
    
    # === PTZ Control ===
    
    def gimbal_up(self, speed: int = 50) -> bool:
        if not self._device_connected or not self._device:
            return False
        speed = max(0, min(100, speed))
        return self._device.set_gimbal_speed(0, speed, 0)
    
    def gimbal_down(self, speed: int = 50) -> bool:
        if not self._device_connected or not self._device:
            return False
        speed = max(0, min(100, speed))
        return self._device.set_gimbal_speed(0, -speed, 0)
    
    def gimbal_left(self, speed: int = 50) -> bool:
        if not self._device_connected or not self._device:
            return False
        speed = max(0, min(100, speed))
        return self._device.set_gimbal_speed(-speed, 0, 0)
    
    def gimbal_right(self, speed: int = 50) -> bool:
        if not self._device_connected or not self._device:
            return False
        speed = max(0, min(100, speed))
        return self._device.set_gimbal_speed(speed, 0, 0)
    
    def stop_gimbal(self) -> bool:
        if not self._device_connected or not self._device:
            return False
        return self._device.stop_gimbal()
    
    def set_zoom(self, level: int) -> bool:
        if not self._device_connected or not self._device:
            return False
        level = max(0, min(100, level))
        self._status.zoom_level = level
        zoom_value = 1.0 + (level / 100.0) * 3.0
        return self._device.set_zoom_absolute(zoom_value)
    
    def zoom_in(self, step: int = 10) -> bool:
        return self.set_zoom(self._status.zoom_level + step)
    
    def zoom_out(self, step: int = 10) -> bool:
        return self.set_zoom(self._status.zoom_level - step)
    
    # === AI Tracking ===
    
    def set_tracking_mode(self, mode: TrackingMode) -> bool:
        if not self._device_connected or not self._device:
            return False
        self._status.tracking_mode = mode
        
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
        
        sub_mode = AiSubMode.Normal
        if mode == TrackingMode.UPPER_BODY:
            sub_mode = AiSubMode.UpperBody
        elif mode == TrackingMode.CLOSEUP:
            sub_mode = AiSubMode.CloseUp
        elif mode == TrackingMode.HEADLESS:
            sub_mode = AiSubMode.HeadHide
        
        result = self._device.set_ai_mode(sdk_mode, sub_mode)
        self._trigger_callbacks('tracking_update', mode)
        return result
    
    def enable_tracking(self, mode: TrackingMode = TrackingMode.NORMAL) -> bool:
        return self.set_tracking_mode(mode)
    
    def disable_tracking(self) -> bool:
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
        if not self._device_connected or not self._device:
            return False
        position_id = max(0, min(9, position_id))
        logger.info(f"Save preset {position_id} - TODO")
        return True
    
    def recall_preset(self, position_id: int) -> bool:
        if not self._device_connected or not self._device:
            return False
        position_id = max(0, min(9, position_id))
        logger.info(f"Recall preset {position_id} - TODO")
        return True
    
    # === Power Management ===
    
    def sleep(self) -> bool:
        if not self._device_connected or not self._device:
            return False
        result = self._device.sleep()
        if result:
            self._status.is_sleeping = True
        return result
    
    def wake_up(self) -> bool:
        if not self._device_connected or not self._device:
            return False
        result = self._device.wake_up()
        if result:
            self._status.is_sleeping = False
        return result
    
    # === Callbacks ===
    
    def on_status_change(self, callback: Callable[[ObsbotStatus], None]):
        self._callbacks['status_change'].append(callback)
    
    def on_tracking_update(self, callback: Callable[[TrackingMode], None]):
        self._callbacks['tracking_update'].append(callback)
    
    def on_error(self, callback: Callable[[str], None]):
        self._callbacks['error'].append(callback)
    
    def _trigger_callbacks(self, event: str, data: Any):
        for callback in self._callbacks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    def get_status(self) -> ObsbotStatus:
        return self._status
    
    def is_connected(self) -> bool:
        return self._device_connected
    
    # === Lifecycle ===
    
    async def shutdown(self):
        logger.info("Shutting down OBSBOT SDK controller...")
        self._running = False
        if self._tracking_task:
            self._tracking_task.cancel()
        if self._sdk:
            self._sdk.shutdown()
            self._sdk = None
        
        self._device = None
        self._device_connected = False
        self._status.connected = False
        logger.info("Shutdown complete")
