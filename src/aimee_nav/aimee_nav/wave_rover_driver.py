#!/usr/bin/env python3
import json
import math
import threading
import time
from typing import Optional

try:
    import serial
except ImportError:
    serial = None

class WaveRoverDriver:
    CMD_SPEED_CTRL = 1
    CMD_VELOCITY = 13

    def __init__(self, port='/dev/ttyACM0', baudrate=115200, wheel_separation=0.26, wheel_radius=0.04, max_speed=0.4, max_angular=1.0, ticks_per_meter=106.0, **kwargs):
        self._port, self._baudrate = port, baudrate
        self._wheel_sep, self._ticks_per_meter = wheel_separation, ticks_per_meter
        self._max_speed, self._max_angular = max_speed, max_angular
        self._serial, self._serial_lock = None, threading.Lock()
        self._running = False
        
        # State for Ramping
        self._last_cmd_linear = 0.0
        self._last_cmd_angular = 0.0
        self._last_cmd_time = time.time()
        self._accel_limit = 0.5 # m/s^2 (1.0s to 0.5m/s)
        self._alpha_limit = 1.0 # rad/s^2
        
        self._last_cmd_L = self._last_cmd_R = 0.0
        self._cmd_active = False
        self._odom_lock = threading.Lock()
        self._x = self._y = self._theta = 0.0
        self._vx = self._vth = 0.0
        self._last_odom_time = time.time()
        self._last_odl = self._last_odr = None

    def is_connected(self): return self._running and self._serial and self._serial.is_open
    def check_watchdog(self): return False

    def connect(self) -> bool:
        try:
            self._serial = serial.Serial(self._port, self._baudrate, timeout=0.1)
            self._running = True
            threading.Thread(target=self._read_loop, daemon=True).start()
            threading.Thread(target=self._command_loop, daemon=True).start()
            return True
        except Exception as e:
            print(f"Connect failed: {e}")
            return False

    def _command_loop(self):
        while self._running:
            if self._cmd_active:
                with self._serial_lock:
                    cmd = {"T": 1, "L": round(self._last_cmd_L, 4), "R": round(self._last_cmd_R, 4)}
                    try:
                        line = json.dumps(cmd) + "\n"
                        self._serial.write(line.encode())
                    except: pass
            time.sleep(0.1)

    def _read_loop(self):
        while self._running:
            try:
                line = self._serial.readline().decode(errors='ignore')
                if not line: continue
                msg = json.loads(line)
                if msg.get('T') == 1001:
                    odl, odr = msg.get('odl'), msg.get('odr')
                    if odl is not None and odr is not None:
                        with self._odom_lock:
                            now = time.time()
                            dt = now - self._last_odom_time
                            if self._last_odl is not None and dt > 0:
                                dl = (int(odl)-self._last_odl)/self._ticks_per_meter
                                dr = (int(odr)-self._last_odr)/self._ticks_per_meter
                                dc, dth = (dl+dr)/2.0, (dr-dl)/self._wheel_sep
                                self._x += dc*math.cos(self._theta); self._y += dc*math.sin(self._theta); self._theta += dth
                                self._vx, self._vth = dc/dt, dth/dt
                            self._last_odl, self._last_odr, self._last_odom_time = int(odl), int(odr), now
            except: pass

    def send_velocity(self, vx, vth):
        now = time.time()
        dt = now - self._last_cmd_time
        self._last_cmd_time = now
        
        # 1. Ramping
        dv_max = self._accel_limit * dt
        dw_max = self._alpha_limit * dt
        
        v_err = vx - self._last_cmd_linear
        w_err = vth - self._last_cmd_angular
        
        vx_ramped = self._last_cmd_linear + max(-dv_max, min(dv_max, v_err))
        vth_ramped = self._last_cmd_angular + max(-dw_max, min(dw_max, w_err))
        
        self._last_cmd_linear = vx_ramped
        self._last_cmd_angular = vth_ramped

        # 2. Kinematics
        vl = vx_ramped - (vth_ramped * self._wheel_sep / 2.0)
        vr = vx_ramped + (vth_ramped * self._wheel_sep / 2.0)
        
        # 3. Normalize (assuming hardware max speed is 1.0)
        L, R = vl / 1.0, vr / 1.0
        MIN_P = 0.18
        mag = max(abs(L), abs(R))
        if 1e-4 < mag < MIN_P:
            scale = MIN_P / mag
            L *= scale
            R *= scale
        self._last_cmd_L, self._last_cmd_R = max(-1, min(1, L)), max(-1, min(1, R))
        self._cmd_active = True

    def stop(self):
        self._last_cmd_L = self._last_cmd_R = 0.0
        self._last_cmd_linear = self._last_cmd_angular = 0.0
        self._cmd_active = False
        if self._serial:
            with self._serial_lock: self._serial.write(b'{"T":1,"L":0,"R":0}\n')

    def disconnect(self):
        self._running = False
        if self._serial: self._serial.close()

    def get_odometry(self):
        with self._odom_lock: return self._x, self._y, self._theta, self._vx, self._vth
