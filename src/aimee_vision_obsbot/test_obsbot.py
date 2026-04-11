#!/usr/bin/env python3
"""
Test script for OBSBOT camera connection and control.

Usage:
    python3 test_obsbot.py

This script tests:
1. USB device detection
2. Network interface detection (RNDIS)
3. OSC connectivity (if available)
4. UVC video capture
5. Basic PTZ commands
"""

import asyncio
import subprocess
import sys
import socket


def check_usb_device():
    """Check if OBSBOT is connected via USB."""
    print("=" * 50)
    print("1. Checking USB Device Detection")
    print("=" * 50)
    
    result = subprocess.run(
        ['lsusb'], capture_output=True, text=True
    )
    
    if 'OBSBOT' in result.stdout:
        for line in result.stdout.split('\n'):
            if 'OBSBOT' in line:
                print(f"✓ Found: {line}")
        return True
    else:
        print("✗ OBSBOT not found in USB devices")
        return False


def check_network_interface():
    """Check for RNDIS network interface."""
    print("\n" + "=" * 50)
    print("2. Checking Network Interface (RNDIS)")
    print("=" * 50)
    
    result = subprocess.run(
        ['ip', 'addr', 'show'], capture_output=True, text=True
    )
    
    # Look for usb0 or interface with 192.168.5.x
    if '192.168.5' in result.stdout:
        print("✓ RNDIS interface found with 192.168.5.x address")
        for line in result.stdout.split('\n'):
            if '192.168.5' in line:
                print(f"  {line.strip()}")
        return True
    else:
        print("✗ No RNDIS interface found (192.168.5.x)")
        print("  The OBSBOT may not expose the control interface")
        print("  or may require different drivers/mode")
        return False


def check_osc_port():
    """Check if OSC port is reachable."""
    print("\n" + "=" * 50)
    print("3. Checking OSC Connectivity (192.168.5.1:16284)")
    print("=" * 50)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('192.168.5.1', 16284))
        sock.close()
        
        if result == 0:
            print("✓ OSC port is reachable!")
            return True
        else:
            print(f"✗ OSC port not reachable (error {result})")
            return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False


def check_uvc():
    """Check UVC video device."""
    print("\n" + "=" * 50)
    print("4. Checking UVC Video Device")
    print("=" * 50)
    
    try:
        import cv2
        
        # Try to open camera index 0
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                height, width = frame.shape[:2]
                print(f"✓ Camera opened successfully")
                print(f"  Resolution: {width}x{height}")
                cap.release()
                return True
            else:
                print("✗ Camera opened but cannot read frames")
                cap.release()
                return False
        else:
            print("✗ Cannot open camera at index 0")
            return False
    except ImportError:
        print("✗ OpenCV (cv2) not installed")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


async def test_brick():
    """Test the ObsbotBrick."""
    print("\n" + "=" * 50)
    print("5. Testing ObsbotBrick")
    print("=" * 50)
    
    try:
        from aimee_vision_obsbot.brick.obsbot_brick import ObsbotBrick
        
        brick = ObsbotBrick(
            control_mode='auto',
            debug=True
        )
        
        print("Initializing brick...")
        await brick.initialize()
        
        print(f"Connected: {brick.is_connected()}")
        print(f"Control mode: {brick.get_control_mode()}")
        
        if brick.is_connected():
            print("\nTesting basic PTZ commands...")
            
            # Test zoom
            print("  - Setting zoom to 50%")
            brick.set_zoom(50)
            await asyncio.sleep(0.5)
            
            # Test gimbal
            print("  - Testing gimbal right")
            brick.gimbal_right(30)
            await asyncio.sleep(0.5)
            
            print("  - Testing gimbal left")
            brick.gimbal_left(30)
            await asyncio.sleep(0.5)
            
            # Test tracking
            print("  - Enabling tracking mode: NORMAL")
            brick.enable_tracking()
            await asyncio.sleep(1.0)
            
            print("  - Disabling tracking")
            brick.disable_tracking()
        
        await brick.shutdown()
        print("\n✓ Brick test completed")
        
    except Exception as e:
        print(f"✗ Brick test error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main test function."""
    print("OBSBOT Camera Test Suite")
    print("=" * 50)
    
    results = {
        'usb': check_usb_device(),
        'network': check_network_interface(),
        'osc': check_osc_port(),
        'uvc': check_uvc(),
    }
    
    # Test brick
    try:
        asyncio.run(test_brick())
        results['brick'] = True
    except Exception as e:
        print(f"\n✗ Brick test failed: {e}")
        results['brick'] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    for test, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {test.upper():12} {status}")
    
    print("\n" + "=" * 50)
    print("Recommendations:")
    print("=" * 50)
    
    if not results['usb']:
        print("- Check USB cable connection")
        print("- Try different USB port")
    
    if not results['network']:
        print("- OBSBOT may need to be in SDK mode")
        print("- Check if RNDIS driver is available")
        print("- Try unplugging and reconnecting camera")
    
    if not results['osc']:
        print("- OSC control requires network interface")
        print("- Alternative: UVC-only mode for basic video")
    
    if not results['uvc']:
        print("- Check camera permissions")
        print("- Install OpenCV: pip install opencv-python")
    
    print("\nFor more info, see OBSBOT SDK documentation")


if __name__ == '__main__':
    main()
