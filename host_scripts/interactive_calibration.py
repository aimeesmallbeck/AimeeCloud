#!/usr/bin/env python3
import serial
import time
import sys
import json
import os

# Configuration
PORT = '/dev/ttyUSB0'
BAUD = 921600
CALIBRATION_FILE = 'arm_physical_limits.json'

class ArmCalibrator:
    def __init__(self):
        try:
            self.ser = serial.Serial(PORT, BAUD, timeout=1)
            print(f"✓ Connected to ESP32 on {PORT}")
        except Exception as e:
            print(f"✗ Error: {e}")
            sys.exit(1)
        
        self.limits = {}

    def send(self, cmd):
        self.ser.write((cmd + '\n').encode('utf-8'))
        self.ser.flush()

    def receive(self):
        start = time.time()
        while time.time() - start < 1.0:
            if self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8').strip()
                if line: return line
        return None

    def get_raw_pos(self):
        # Clear buffer
        while self.ser.in_waiting: self.ser.read(self.ser.in_waiting)
        self.send("READ")
        resp = self.receive()
        if resp and resp.startswith("POS:<") and resp.endswith(">"):
            return resp[5:-1].split(',')
        return None

    def calibrate_step(self, key, prompt):
        print(f"\n[STEP] {prompt}")
        input(">> Position the arm and press ENTER to capture...")
        pos = self.get_raw_pos()
        if pos:
            self.limits[key] = pos
            print(f"✓ Captured {key}: {pos}")
        else:
            print("✗ Failed to read position. Retrying...")
            self.calibrate_step(key, prompt)

    def run(self):
        print("="*60)
        print("ROARM-M3 PHYSICAL CALIBRATION WIZARD")
        print("="*60)
        
        self.send("PING")
        if self.receive() != "PONG":
            print("✗ ESP32 not responding. Check connection.")
            return

        print("\n[WARNING] Disabling torque. HOLD THE ARM NOW.")
        input("Press ENTER when ready to release motors...")
        self.send("FREEZE")
        if self.receive() != "FROZEN":
            print("✗ Failed to freeze motors.")
            return

        # 1. Floor Limit (Safety Z)
        self.calibrate_step("floor_limit", "Place the gripper on the table (or lowest safe height).")
        
        # 2. Reach Limit (Safety Radius)
        self.calibrate_step("max_reach", "Extend the arm to the MAXIMUM safe forward reach.")
        
        # 3. Minimum Reach (Base avoidance)
        self.calibrate_step("min_reach", "Tuck the arm to the MINIMUM safe distance from the base.")

        # 4. Gripper Open
        self.calibrate_step("gripper_open", "Manually open the gripper to its FULL open position.")

        # 5. Gripper Closed
        self.calibrate_step("gripper_closed", "Manually close the gripper to its FULL closed position.")

        # 6. Home Position
        self.calibrate_step("home_position", "Move the arm to your preferred HOME/READY position.")

        # Save results
        with open(CALIBRATION_FILE, 'w') as f:
            json.dump(self.limits, f, indent=2)
        
        print("\n" + "="*60)
        print(f"✓ CALIBRATION COMPLETE! Data saved to {CALIBRATION_FILE}")
        print("="*60)
        print("\nYou can now reconnect the STM32 RX/TX pins.")

if __name__ == "__main__":
    ArmCalibrator().run()
