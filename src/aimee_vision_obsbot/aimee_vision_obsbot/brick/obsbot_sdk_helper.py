#!/usr/bin/env python3
"""
OBSBOT SDK wrapper using C++ helper program
"""

import subprocess
import logging
import os
from enum import IntEnum
from typing import Optional

logger = logging.getLogger(__name__)

HELPER_PATH = "/workspace/obsbot_helper/obsbot_ctrl"


class AiWorkMode(IntEnum):
    None_ = 0
    Group = 1
    Human = 2
    Hand = 3
    WhiteBoard = 4
    Desk = 5


class AiSubMode(IntEnum):
    Normal = 0
    UpperBody = 1
    CloseUp = 2
    HeadHide = 3
    LowerBody = 4


class DevStatus(IntEnum):
    Error = -1
    Run = 1
    Sleep = 3
    Privacy = 4


class ObsbotDeviceHelper:
    """OBSBOT device control using C++ helper subprocess."""
    
    def __init__(self, sn: str = ""):
        self._sn = sn
        self._helper = HELPER_PATH
        if not os.path.exists(self._helper):
            # Try local path
            self._helper = "/home/arduino/aimee-robot-ws/obsbot_helper/obsbot_ctrl"
    
    def _call(self, *args) -> tuple:
        """Call helper program."""
        cmd = [self._helper] + list(args)
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10
            )
            logger.debug(f"Helper: {' '.join(args)} -> {result.returncode}")
            if result.returncode != 0:
                logger.error(f"Helper error: {result.stderr}")
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            logger.error(f"Helper call error: {e}")
            return -1, "", str(e)
    
    def get_sn(self) -> str:
        return self._sn
    
    def set_gimbal_speed(self, yaw: float, pitch: float, roll: float = 0.0) -> bool:
        """Set gimbal speed."""
        ret, out, err = self._call("gimbal", str(yaw), str(pitch), str(roll))
        return ret == 0
    
    def set_gimbal_motor_angle(self, yaw: float, pitch: float, roll: float = 0.0) -> bool:
        """Set absolute motor angle."""
        # Not implemented in helper
        return False
    
    def stop_gimbal(self) -> bool:
        """Stop gimbal."""
        ret, out, err = self._call("stop")
        return ret == 0
    
    def set_zoom_absolute(self, zoom: float, speed: int = 6) -> bool:
        """Set zoom level (1.0-4.0)."""
        ret, out, err = self._call("zoom", str(zoom))
        return ret == 0
    
    def set_ai_mode(self, mode: AiWorkMode, sub_mode: AiSubMode = AiSubMode.Normal) -> bool:
        """Set AI tracking mode."""
        ret, out, err = self._call("aimode", str(int(mode)), str(int(sub_mode)))
        return ret == 0
    
    def set_device_status(self, status: DevStatus) -> bool:
        """Set device status."""
        if status == DevStatus.Run:
            ret, _, _ = self._call("wakeup")
        elif status == DevStatus.Sleep:
            ret, _, _ = self._call("sleep")
        else:
            return False
        return ret == 0
    
    def wake_up(self) -> bool:
        return self.set_device_status(DevStatus.Run)
    
    def sleep(self) -> bool:
        return self.set_device_status(DevStatus.Sleep)


class ObsbotSDKHelper:
    """SDK wrapper using helper program."""
    
    def __init__(self, sdk_path: str = ""):
        self._helper = HELPER_PATH
        if not os.path.exists(self._helper):
            self._helper = "/home/arduino/aimee-robot-ws/obsbot_helper/obsbot_ctrl"
        self._device: Optional[ObsbotDeviceHelper] = None
    
    def initialize(self) -> bool:
        """Initialize SDK (helper handles this)."""
        if not os.path.exists(self._helper):
            logger.error(f"Helper not found: {self._helper}")
            return False
        return True
    
    def scan_devices(self, wait: bool = True) -> list:
        """Scan for devices."""
        devices = []
        retries = 3 if wait else 1
        
        for i in range(retries):
            try:
                result = subprocess.run(
                    [self._helper, "list"],
                    capture_output=True, text=True, timeout=10
                )
                if "Device SN:" in result.stdout:
                    for line in result.stdout.split('\n'):
                        if "Device SN:" in line:
                            sn = line.split(":")[1].strip()
                            devices.append({'sn': sn})
                    if devices:
                        break
                elif i < retries - 1:
                    import time
                    time.sleep(2)  # Wait for device detection
            except Exception as e:
                logger.error(f"Scan error: {e}")
        
        return devices
    
    def is_tiny2_lite_connected(self) -> bool:
        """Check if Tiny 2 Lite is connected."""
        devices = self.scan_devices()
        return len(devices) > 0
    
    def get_device_count(self) -> int:
        """Get device count."""
        return len(self.scan_devices())
    
    def get_first_device(self) -> Optional[ObsbotDeviceHelper]:
        """Get first device."""
        devices = self.scan_devices()
        if devices:
            sn = devices[0].get('sn', '')
            self._device = ObsbotDeviceHelper(sn)
            return self._device
        return None
    
    def shutdown(self):
        """Cleanup."""
        self._device = None
