#!/usr/bin/env python3
"""
OBSBOT SDK wrapper using C++ helper program
"""

import subprocess
import logging
import os
import socket
import threading
import time
from enum import IntEnum
from typing import Optional

logger = logging.getLogger(__name__)

HELPER_PATH = "/workspace/obsbot_helper/obsbot_ctrl"
SDK_LIB_DIR = "/workspace/libdev_v2.1.0_8/linux/arm64-release"
_DAEMON_SOCKET = "/tmp/obsbot_daemon.sock"
_DAEMON_PROC = None
_DAEMON_LOCK = threading.Lock()


def _ensure_daemon():
    """Start the persistent obsbot_ctrl daemon if not running."""
    global _DAEMON_PROC
    with _DAEMON_LOCK:
        if _DAEMON_PROC is not None and _DAEMON_PROC.poll() is None:
            return
        # Clean up old socket
        try:
            os.unlink(_DAEMON_SOCKET)
        except FileNotFoundError:
            pass
        if not os.path.exists(HELPER_PATH):
            logger.error(f"Helper not found: {HELPER_PATH}")
            return
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = SDK_LIB_DIR + ":" + env.get("LD_LIBRARY_PATH", "")
        logger.info("Starting obsbot_ctrl daemon...")
        _DAEMON_PROC = subprocess.Popen(
            [HELPER_PATH, "daemon", _DAEMON_SOCKET],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )
        # Wait for socket file to appear
        for _ in range(60):
            if os.path.exists(_DAEMON_SOCKET):
                logger.info("Daemon ready")
                return
            time.sleep(0.1)
        logger.error("Daemon failed to start")
        _DAEMON_PROC = None


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
        """Call helper program via daemon socket, with fallback to single-shot."""
        _ensure_daemon()
        with _DAEMON_LOCK:
            try:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.settimeout(2.0)
                sock.connect(_DAEMON_SOCKET)
                cmd_line = " ".join(args) + "\n"
                sock.sendall(cmd_line.encode())
                resp = sock.recv(16).decode().strip()
                sock.close()
                rc = 0 if resp == "OK" else 1
                logger.debug(f"Daemon call: {' '.join(args)} -> {resp}")
                return rc, "", ""
            except Exception as e:
                logger.warning(f"Daemon call failed, falling back to single-shot: {e}")
        
        # Fallback: single-shot subprocess
        cmd = [self._helper] + list(args)
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = SDK_LIB_DIR + ":" + env.get("LD_LIBRARY_PATH", "")
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10, env=env, close_fds=True
            )
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
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = SDK_LIB_DIR + ":" + env.get("LD_LIBRARY_PATH", "")
        
        for i in range(retries):
            try:
                result = subprocess.run(
                    [self._helper, "list"],
                    capture_output=True, text=True, timeout=10, env=env
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
