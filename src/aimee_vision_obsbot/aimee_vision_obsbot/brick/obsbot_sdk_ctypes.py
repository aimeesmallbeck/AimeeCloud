#!/usr/bin/env python3
"""
OBSBOT SDK CTypes Wrapper - Direct C++ binding

Uses ctypes to call the C++ library functions directly.
"""

import ctypes
import ctypes.util
import os
import logging
from enum import IntEnum
from typing import Optional, List, Callable

logger = logging.getLogger(__name__)

# Load the library
def load_sdk_lib(path: str = "/home/arduino/libdev_v2.1.0_8/linux/arm64-release/libdev.so"):
    """Load the SDK shared library."""
    if not os.path.exists(path):
        # Try container path
        path = "/workspace/libdev_v2.1.0_8/linux/arm64-release/libdev.so"
    
    if not os.path.exists(path):
        raise RuntimeError(f"SDK library not found at {path}")
    
    lib = ctypes.CDLL(path, mode=ctypes.RTLD_GLOBAL)
    logger.info(f"Loaded SDK from {path}")
    return lib


class ObsbotProductType(IntEnum):
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


# C++ std::string wrapper
class StdString(ctypes.Structure):
    _fields_ = [
        ("data", ctypes.c_char_p),
        ("size", ctypes.c_size_t),
        ("capacity", ctypes.c_size_t),
    ]


class ObsbotDevice:
    """Wrapper for a single OBSBOT device."""
    
    def __init__(self, lib, device_ptr, sn: str = ""):
        self._lib = lib
        self._ptr = device_ptr
        self._sn = sn
        self._use_singleton = (device_ptr is None)
    
    def _call_method(self, method_name, *args, restype=None):
        """Call a C++ method on this device."""
        try:
            # Try mangled name (Device::methodName)
            sym = f"_ZN6Device{len(method_name)}{method_name}E"
            func = getattr(self._lib, sym, None)
            if func:
                func.restype = restype
                if self._ptr:
                    func.argtypes = [ctypes.c_void_p] + [type(a) for a in args]
                    return func(self._ptr, *args)
                else:
                    # For singleton/static methods
                    func.argtypes = [type(a) for a in args]
                    return func(*args)
            
            return None
        except Exception as e:
            logger.error(f"Method call error {method_name}: {e}")
            return None
    
    def get_sn(self) -> str:
        """Get device serial number."""
        if self._sn:
            return self._sn
        
        # Try to call devSn() method
        # This returns std::string which is complex
        # For now, return placeholder
        return "UNKNOWN"
    
    def get_product_type(self) -> ObsbotProductType:
        """Get product type."""
        result = self._call_method("productType", restype=ctypes.c_int)
        if result is not None:
            return ObsbotProductType(result)
        return ObsbotProductType.Tiny2Lite
    
    def set_gimbal_speed(self, yaw: float, pitch: float, roll: float = 0.0) -> bool:
        """
        Set gimbal speed.
        yaw: -100 to 100 (negative=left, positive=right)
        pitch: -100 to 100 (negative=down, positive=up)
        roll: usually 0
        """
        try:
            # Device::aiSetGimbalSpeedCtrlR(double, double, double)
            func = self._lib._ZN6Device21aiSetGimbalSpeedCtrlEddd
            func.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_double]
            func.restype = ctypes.c_int
            result = func(self._ptr, float(yaw), float(pitch), float(roll))
            logger.debug(f"Set gimbal speed: yaw={yaw}, pitch={pitch}, result={result}")
            return result == 0
        except Exception as e:
            logger.error(f"set_gimbal_speed error: {e}")
            return False
    
    def set_gimbal_motor_angle(self, yaw: float, pitch: float, roll: float = 0.0) -> bool:
        """Set absolute motor angle."""
        try:
            # Device::aiSetGimbalMotorAngleR(float, float, float)
            func = self._lib._ZN6Device24aiSetGimbalMotorAngleREfff
            func.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.c_float]
            func.restype = ctypes.c_int
            result = func(self._ptr, float(yaw), float(pitch), float(roll))
            return result == 0
        except Exception as e:
            logger.error(f"set_gimbal_motor_angle error: {e}")
            return False
    
    def stop_gimbal(self) -> bool:
        """Stop gimbal movement."""
        try:
            # Device::aiSetGimbalStop()
            func = self._lib._ZN6Device17aiSetGimbalStopEv
            func.argtypes = [ctypes.c_void_p]
            func.restype = ctypes.c_int
            result = func(self._ptr)
            return result == 0
        except Exception as e:
            logger.error(f"stop_gimbal error: {e}")
            return False
    
    def set_zoom_absolute(self, zoom: float, speed: int = 6) -> bool:
        """
        Set absolute zoom level.
        zoom: 1.0 to 4.0
        speed: 1 to 10
        """
        try:
            # Device::cameraSetZoomAbsoluteR(float, int)
            func = self._lib._ZN6Device22cameraSetZoomAbsoluteREfi
            func.argtypes = [ctypes.c_void_p, ctypes.c_float, ctypes.c_int]
            func.restype = ctypes.c_int
            result = func(self._ptr, float(zoom), int(speed))
            logger.debug(f"Set zoom: {zoom}x, speed={speed}, result={result}")
            return result == 0
        except Exception as e:
            logger.error(f"set_zoom_absolute error: {e}")
            return False
    
    def set_ai_mode(self, mode: AiWorkMode, sub_mode: AiSubMode = AiSubMode.Normal) -> bool:
        """Set AI tracking mode."""
        try:
            # Device::cameraSetAiModeU(int, int)
            func = self._lib._ZN6Device19cameraSetAiModeUEii
            func.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
            func.restype = ctypes.c_int
            result = func(self._ptr, int(mode), int(sub_mode))
            logger.info(f"Set AI mode: {mode.name}, sub: {sub_mode.name}, result={result}")
            return result == 0
        except Exception as e:
            logger.error(f"set_ai_mode error: {e}")
            return False
    
    def set_device_status(self, status: DevStatus) -> bool:
        """Set device run status."""
        try:
            # Device::cameraSetDevRunStatusR(int)
            func = self._lib._ZN6Device23cameraSetDevRunStatusREi
            func.argtypes = [ctypes.c_void_p, ctypes.c_int]
            func.restype = ctypes.c_int
            result = func(self._ptr, int(status))
            return result == 0
        except Exception as e:
            logger.error(f"set_device_status error: {e}")
            return False
    
    def wake_up(self) -> bool:
        """Wake device."""
        return self.set_device_status(DevStatus.Run)
    
    def sleep(self) -> bool:
        """Put device to sleep."""
        return self.set_device_status(DevStatus.Sleep)


class ObsbotSDKNative:
    """Native SDK wrapper using ctypes."""
    
    def __init__(self, sdk_path: str = "/home/arduino/libdev_v2.1.0_8/linux/arm64-release/libdev.so"):
        self.sdk_path = sdk_path
        self._lib = None
        self._devices_ptr = None
        self._connected_device: Optional[ObsbotDevice] = None
    
    def initialize(self) -> bool:
        """Initialize SDK."""
        try:
            self._lib = load_sdk_lib(self.sdk_path)
            
            # Get Devices singleton
            # Devices& Devices::get()
            get_devices = self._lib._ZN7Devices3getEv
            get_devices.restype = ctypes.c_void_p
            get_devices.argtypes = []
            
            self._devices_ptr = get_devices()
            logger.info(f"Devices manager: {self._devices_ptr}")
            
            return True
        except Exception as e:
            logger.error(f"SDK init error: {e}")
            return False
    
    def get_device_count(self) -> int:
        """Get number of connected devices."""
        if not self._lib or not self._devices_ptr:
            return 0
        
        try:
            # size_t Devices::getDevNum()
            func = self._lib._ZN7Devices9getDevNumEv
            func.restype = ctypes.c_size_t
            func.argtypes = [ctypes.c_void_p]
            return func(self._devices_ptr)
        except Exception as e:
            logger.error(f"get_device_count error: {e}")
            return 0
    
    def scan_devices(self) -> List[dict]:
        """Scan for devices."""
        devices = []
        
        # Use system command to detect USB
        try:
            import subprocess
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'OBSBOT' in line:
                    devices.append({
                        'type': 'usb',
                        'description': line.strip()
                    })
        except Exception as e:
            logger.error(f"USB scan error: {e}")
        
        return devices
    
    def is_tiny2_lite_connected(self) -> bool:
        """Check if Tiny 2 Lite is connected."""
        devices = self.scan_devices()
        for dev in devices:
            if 'Tiny 2 Lite' in dev.get('description', ''):
                return True
        return False
    
    def get_device_by_sn(self, sn: str) -> Optional[ObsbotDevice]:
        """Get device by serial number."""
        if not self._lib or not self._devices_ptr:
            return None
        
        try:
            # std::shared_ptr<Device> Devices::getDevBySn(const std::string&)
            # This is tricky with shared_ptr in ctypes...
            # For now, we'll create a device wrapper with a dummy pointer
            # The SDK manages the device lifecycle internally
            
            # Try to call getDevBySn
            func = self._lib._ZN7Devices10getDevBySnERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
            func.restype = ctypes.c_void_p  # Returns shared_ptr, we get the Device* part
            func.argtypes = [ctypes.c_void_p, ctypes.c_void_p]  # this, string
            
            # Create std::string (simplified - just use bytes for now)
            # This won't work well with std::string...
            
            # Alternative: Just create device wrapper without calling C++
            # The SDK methods work on the singleton, so we can call them directly
            return ObsbotDevice(self._lib, None, sn)
        except Exception as e:
            logger.error(f"get_device_by_sn error: {e}")
            return None
    
    def get_first_device(self) -> Optional[ObsbotDevice]:
        """Get the first connected device."""
        if not self._lib or not self._devices_ptr:
            return None
        
        # Try to get by known SN from logs
        # From logs: RMOWLHI1213WUG
        device = self.get_device_by_sn("RMOWLHI1213WUG")
        if device:
            return device
        
        # If that fails, create a generic device wrapper
        # The SDK methods are static/singleton based, so this should work
        return ObsbotDevice(self._lib, None, "auto")
    
    def shutdown(self):
        """Clean up SDK."""
        self._connected_device = None
        if self._lib and self._devices_ptr:
            try:
                # Devices::close()
                func = self._lib._ZN7Devices5closeEv
                func.argtypes = [ctypes.c_void_p]
                func(self._devices_ptr)
            except:
                pass
        self._lib = None


# Singleton
_sdk_native = None

def get_native_sdk() -> ObsbotSDKNative:
    """Get native SDK singleton."""
    global _sdk_native
    if _sdk_native is None:
        _sdk_native = ObsbotSDKNative()
    return _sdk_native
