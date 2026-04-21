#!/usr/bin/env python3
"""
OBSBOT SDK Python Wrapper using ctypes

Wraps the libdev.so C++ SDK for ARM64 Linux.
"""

import ctypes
import ctypes.util
import os
import logging
from enum import IntEnum
from typing import Optional, Callable, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Path to SDK library
SDK_PATH = "/home/arduino/libdev_v2.1.0_8/linux/arm64-release/libdev.so"


class ObsbotProductType(IntEnum):
    """OBSBOT product types."""
    Tiny = 0
    Tiny4k = 1
    Tiny2 = 2
    Tiny2Lite = 3
    TailAir = 4
    Meet = 5
    Meet4k = 6
    Me = 7
    HDMIBox = 8
    NDIBox = 9
    Meet2 = 10
    Tail2 = 11
    TinySE = 12
    MeetSE = 13
    Tail2S = 16
    Tiny3 = 18
    Tiny3Lite = 19


class AiWorkMode(IntEnum):
    """AI work modes for Tiny2 series."""
    None_ = 0
    Group = 1
    Human = 2
    Hand = 3
    WhiteBoard = 4
    Desk = 5
    Switching = 6


class AiSubMode(IntEnum):
    """AI sub modes for human tracking."""
    Normal = 0
    UpperBody = 1
    CloseUp = 2
    HeadHide = 3
    LowerBody = 4


class DevStatus(IntEnum):
    """Device status."""
    Error = -1
    Run = 1
    Sleep = 3
    Privacy = 4


@dataclass
class PresetPosInfo:
    """Preset position info."""
    id: int = 0
    name: str = ""
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    zoom: float = 1.0


class ObsbotSDK:
    """
    OBSBOT SDK wrapper using ctypes.
    
    This wraps the C++ libdev.so library for Python use.
    """
    
    def __init__(self, sdk_path: str = SDK_PATH):
        """Initialize SDK wrapper."""
        self.sdk_path = sdk_path
        self._lib: Optional[ctypes.CDLL] = None
        self._initialized = False
        self._devices = []
        
        # Callbacks
        self._dev_changed_cb: Optional[Callable] = None
        self._status_cb: Optional[Callable] = None
        
    def initialize(self) -> bool:
        """Load and initialize the SDK library."""
        try:
            if not os.path.exists(self.sdk_path):
                logger.error(f"SDK library not found: {self.sdk_path}")
                return False
            
            self._lib = ctypes.CDLL(self.sdk_path)
            logger.info(f"Loaded SDK from {self.sdk_path}")
            
            # Initialize devices manager
            self._init_devices()
            
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize SDK: {e}")
            return False
    
    def _init_devices(self):
        """Initialize device detection."""
        # The SDK uses a singleton Devices class
        # We need to call Devices::get() to get the instance
        # For now, we'll use a simpler approach - scan for devices
        pass
    
    def scan_devices(self) -> List[dict]:
        """
        Scan for connected OBSBOT devices.
        
        Returns list of device info dicts.
        """
        devices = []
        
        # Check for UVC devices
        try:
            import subprocess
            result = subprocess.run(
                ['lsusb'], capture_output=True, text=True
            )
            
            for line in result.stdout.split('\n'):
                if 'OBSBOT' in line:
                    # Parse device info
                    parts = line.split()
                    if len(parts) >= 6:
                        devices.append({
                            'type': 'usb',
                            'description': line.strip(),
                            'id': parts[5] if len(parts) > 5 else 'unknown'
                        })
        except Exception as e:
            logger.error(f"Device scan error: {e}")
        
        self._devices = devices
        return devices
    
    def get_device_count(self) -> int:
        """Get number of connected devices."""
        return len(self.scan_devices())
    
    def is_tiny2_lite_connected(self) -> bool:
        """Check if Tiny 2 Lite is connected."""
        devices = self.scan_devices()
        for dev in devices:
            if 'Tiny 2 Lite' in dev.get('description', ''):
                return True
        return False
    
    # === PTZ Control ===
    
    def set_gimbal_speed(self, yaw_speed: int, pitch_speed: int, roll_speed: int = 0) -> bool:
        """
        Set gimbal movement speed.
        
        Speed range: typically -100 to 100
        Set to 0 to stop movement.
        """
        # Placeholder - would call SDK function
        # aiSetGimbalSpeedCtrlR(yaw_speed, pitch_speed, roll_speed)
        logger.debug(f"Set gimbal speed: yaw={yaw_speed}, pitch={pitch_speed}")
        return True
    
    def set_gimbal_angle(self, yaw: float, pitch: float, roll: float = 0.0) -> bool:
        """
        Move gimbal to absolute angle.
        
        Angles in degrees.
        """
        # Placeholder - would call SDK function
        # aiSetGimbalMotorAngleR(yaw, pitch, roll)
        logger.debug(f"Set gimbal angle: yaw={yaw}, pitch={pitch}, roll={roll}")
        return True
    
    def stop_gimbal(self) -> bool:
        """Stop gimbal movement."""
        return self.set_gimbal_speed(0, 0, 0)
    
    # === Zoom Control ===
    
    def set_zoom_absolute(self, zoom: float) -> bool:
        """
        Set absolute zoom level.
        
        zoom: 1.0 to 4.0 (1x to 4x)
        """
        # Placeholder - would call SDK function
        # cameraSetZoomAbsoluteR(zoom)
        logger.debug(f"Set zoom: {zoom}x")
        return True
    
    def set_zoom_with_speed(self, zoom: float, speed: int) -> bool:
        """
        Set zoom with specified speed.
        
        zoom: 1.0 to 4.0
        speed: 1 to 10
        """
        # Placeholder - would call SDK function
        # cameraSetZoomWithSpeedAbsoluteR(zoom * 100, speed)
        logger.debug(f"Set zoom: {zoom}x, speed={speed}")
        return True
    
    # === AI Tracking ===
    
    def set_ai_mode(self, mode: AiWorkMode, sub_mode: AiSubMode = AiSubMode.Normal) -> bool:
        """
        Set AI tracking mode.
        
        For Tiny 2 Lite, this enables/disables tracking.
        """
        # Placeholder - would call SDK function
        # cameraSetAiModeU(mode, sub_mode)
        logger.info(f"Set AI mode: {mode.name}, sub_mode: {sub_mode.name}")
        return True
    
    def enable_tracking(self, mode: AiWorkMode = AiWorkMode.Human) -> bool:
        """Enable AI tracking."""
        return self.set_ai_mode(mode)
    
    def disable_tracking(self) -> bool:
        """Disable AI tracking."""
        return self.set_ai_mode(AiWorkMode.None_)
    
    def set_tracking_sub_mode(self, sub_mode: AiSubMode) -> bool:
        """Set tracking sub-mode (e.g., upper body, closeup)."""
        return self.set_ai_mode(AiWorkMode.Human, sub_mode)
    
    # === Presets ===
    
    def save_preset(self, preset_id: int, name: str = "") -> bool:
        """Save current position as preset (0-9)."""
        # Placeholder - would call SDK function
        # aiAddGimbalPresetR(&presetInfo)
        logger.info(f"Save preset {preset_id}: {name}")
        return True
    
    def recall_preset(self, preset_id: int) -> bool:
        """Move to saved preset position."""
        # Placeholder - would call SDK function
        # aiTrgGimbalPresetR(preset_id)
        logger.info(f"Recall preset {preset_id}")
        return True
    
    def set_boot_position(self, yaw: float, pitch: float, roll: float, zoom: float) -> bool:
        """Set boot/startup position."""
        # Placeholder - would call SDK function
        # aiSetGimbalBootPosR(presetInfo)
        logger.info(f"Set boot position: yaw={yaw}, pitch={pitch}, zoom={zoom}")
        return True
    
    def move_to_boot_position(self) -> bool:
        """Move to boot/startup position."""
        # Placeholder - would call SDK function
        # aiTrgGimbalBootPosR()
        logger.info("Move to boot position")
        return True
    
    # === Device State ===
    
    def set_device_status(self, status: DevStatus) -> bool:
        """
        Set device status (run, sleep, etc.).
        """
        # Placeholder - would call SDK function
        # cameraSetDevRunStatusR(status)
        logger.info(f"Set device status: {status.name}")
        return True
    
    def wake_up(self) -> bool:
        """Wake device from sleep."""
        return self.set_device_status(DevStatus.Run)
    
    def sleep(self) -> bool:
        """Put device to sleep."""
        return self.set_device_status(DevStatus.Sleep)
    
    def privacy_mode(self, enable: bool) -> bool:
        """Enable/disable privacy mode."""
        status = DevStatus.Privacy if enable else DevStatus.Run
        return self.set_device_status(status)
    
    # === Camera Settings ===
    
    def set_hdr(self, enable: bool) -> bool:
        """Enable/disable HDR."""
        # Placeholder
        logger.info(f"Set HDR: {enable}")
        return True
    
    def set_face_focus(self, enable: bool) -> bool:
        """Enable/disable face focus priority."""
        # Placeholder - would call SDK function
        # cameraSetFaceFocusR(enable)
        logger.info(f"Set face focus: {enable}")
        return True
    
    def set_manual_focus(self, value: int) -> bool:
        """
        Set manual focus value.
        
        value: 0-100
        """
        # Placeholder - would call SDK function
        # cameraSetFocusAbsolute(value, False)
        logger.info(f"Set manual focus: {value}")
        return True
    
    # === Callbacks ===
    
    def set_device_changed_callback(self, callback: Callable[[str, bool], None]):
        """Set callback for device connect/disconnect events."""
        self._dev_changed_cb = callback
    
    def set_status_callback(self, callback: Callable[[dict], None]):
        """Set callback for status updates."""
        self._status_cb = callback
    
    # === Cleanup ===
    
    def shutdown(self):
        """Clean up SDK resources."""
        self._initialized = False
        self._lib = None
        logger.info("SDK shutdown")


# Singleton instance
_sdk_instance: Optional[ObsbotSDK] = None


def get_sdk() -> ObsbotSDK:
    """Get SDK singleton instance."""
    global _sdk_instance
    if _sdk_instance is None:
        _sdk_instance = ObsbotSDK()
    return _sdk_instance
