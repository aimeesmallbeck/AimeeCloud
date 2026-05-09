/**
 * STM32U585 "Real-Time Trajectory Engine" Firmware
 * Phase 4 of the AimeeCloud Dual-Core Pipeline.
 * 
 * Runs on the UNO Q's STM32 co-processor.
 * Uses Arduino_RouterBridge to receive RPC commands from the ARM64.
 * Computes a smooth minimum-jerk (quintic) trajectory.
 * Streams micro-waypoints at 50Hz (20ms) to the ESP32 via Hardware Serial.
 * 
 * UPGRADED: Added support for 'Raw' streaming (fluid motion) and 'Freeze' (limp mode).
 */

#include <Arduino.h>
#include <bridge.h>
#include <math.h>

// Number of joints
#define NUM_JOINTS 6

// Hardware Serial connected to ROArm ESP32
#define ARM_BAUD_RATE 921600

// 50Hz sampling -> 20ms period
#define TICK_RATE_MS 20

// State for each joint
struct JointState {
  float current_pos;
  float start_pos;
  float target_pos;
  float duration; // Time to reach target in ms
  float elapsed;  // Time elapsed in ms
  bool active;
};

JointState joints[NUM_JOINTS];

// Initialize at the calibrated home position: Base, Shoulder, Elbow, Wrist, Roll, Gripper
int home_pos[NUM_JOINTS] = {2056, 2060, 2636, 2484, 2043, 2062};

// Set target for all joints (Starts a quintic trajectory)
void set_target_joints(int j1, int j2, int j3, int j4, int j5, int j6, int duration_ms) {
  // STRICT HARDWARE SAFETY LIMITS
  // Base: Prevent moving past 90 degrees left or right (2048 +/- 1024)
  if (j1 < 1024) j1 = 1024;
  if (j1 > 3072) j1 = 3072;
  
  // Shoulder: Prevent moving past vertical (backward)
  // 2048 is vertical. Greater values move forward/down.
  if (j2 < 2048) j2 = 2048;

  int values[6] = {j1, j2, j3, j4, j5, j6};
  float duration = (float)duration_ms;
  if (duration < TICK_RATE_MS) duration = TICK_RATE_MS;
  
  for (int i = 0; i < NUM_JOINTS; i++) {
    joints[i].start_pos = joints[i].current_pos;
    joints[i].target_pos = values[i];
    joints[i].duration = duration;
    joints[i].elapsed = 0;
    joints[i].active = true;
  }
}

// Bypasses the quintic trajectory for high-frequency streaming from host
void stream_waypoints(int j1, int j2, int j3, int j4, int j5, int j6) {
  // STRICT HARDWARE SAFETY LIMITS
  if (j1 < 1024) j1 = 1024;
  if (j1 > 3072) j1 = 3072;
  if (j2 < 2048) j2 = 2048;

  int values[6] = {j1, j2, j3, j4, j5, j6};
  for (int i = 0; i < NUM_JOINTS; i++) {
    joints[i].active = false; // Stop any active quintic movement
    joints[i].current_pos = (float)values[i];
    joints[i].target_pos = (float)values[i];
  }
}

// RPC Callback for Raw Waypoints (Standard Smooth)
void receive_waypoints(int j1, int j2, int j3, int j4, int j5, int j6, int duration_ms) {
  set_target_joints(j1, j2, j3, j4, j5, j6, duration_ms);
}

// Inverse Kinematics Mapping
void ik_map(float x, float y, float z, float pitch, float gripper_width, int* out_raw) {
  float L1 = 0.12606;
  float L2 = 0.23871;
  float t2rad = 0.1259;
  float L3 = 0.14449;
  float t3rad = 0.0;
  float LE = 0.17221;
  float tErad = 0.0795;

  float r_target = sqrt(x*x + y*y);
  float yaw = atan2(y, x);

  float SAFE_WRIST_Z_MIN = -0.088;
  if (z < SAFE_WRIST_Z_MIN) z = SAFE_WRIST_Z_MIN;
      
  float MIN_REACH = 0.10;
  if (r_target < MIN_REACH) {
      float scale = (r_target > 0) ? (MIN_REACH / r_target) : MIN_REACH;
      x *= scale; y *= scale; r_target = MIN_REACH;
  }

  float angleE = -pitch - tErad;
  float r_wrist = r_target - LE * cos(angleE);
  float z_wrist = z - L1 - LE * sin(angleE);

  float LA = L2;
  float LB = L3;
  float aIn = r_wrist;
  float bIn = z_wrist;
  float L2C = aIn*aIn + bIn*bIn;
  float LC = sqrt(L2C);
  
  if (LC > (LA + LB)) {
      float scale = (LA + LB - 0.001) / LC;
      aIn *= scale; bIn *= scale; L2C = aIn*aIn + bIn*bIn; LC = sqrt(L2C);
  }

  float lambda_ang = atan2(bIn, aIn);
  float cos_psi = (LA*LA + L2C - LB*LB) / (2 * LA * LC);
  if (cos_psi < -1.0) cos_psi = -1.0; else if (cos_psi > 1.0) cos_psi = 1.0;
  float psi = acos(cos_psi) + t2rad;

  float alpha = M_PI / 2.0 - lambda_ang - psi;

  float cos_omega = (LB*LB + L2C - LA*LA) / (2 * LC * LB);
  if (cos_omega < -1.0) cos_omega = -1.0; else if (cos_omega > 1.0) cos_omega = 1.0;
  float omega = acos(cos_omega);

  float beta = psi + omega - t3rad;
  float w_rad = pitch - alpha - beta + M_PI/2.0;

  out_raw[0] = (int)(2047 - (yaw * 2048.0 / M_PI));
  if (out_raw[0] < 1023) out_raw[0] = 1023; else if (out_raw[0] > 3071) out_raw[0] = 3071;
  
  out_raw[1] = (int)(2047 + alpha * 2048.0 / M_PI);
  if (out_raw[1] < 2047) out_raw[1] = 2047; else if (out_raw[1] > 4095) out_raw[1] = 4095;
  
  out_raw[2] = (int)(1024 + beta * 2048.0 / M_PI);
  if (out_raw[2] < 0) out_raw[2] = 0; else if (out_raw[2] > 4095) out_raw[2] = 4095;
  
  out_raw[3] = (int)(2047 + w_rad * 2048.0 / M_PI);
  if (out_raw[3] < 0) out_raw[3] = 0; else if (out_raw[3] > 4095) out_raw[3] = 4095;

  float w_clamped = gripper_width;
  if (w_clamped < 0.0) w_clamped = 0.0; else if (w_clamped > 0.08) w_clamped = 0.08;
  
  if (w_clamped <= 0.005) out_raw[5] = 2061;
  else if (w_clamped >= 0.075) out_raw[5] = 853;
  else out_raw[5] = (int)(2061 - (w_clamped * 15100.0));
  
  out_raw[4] = 2043; // Default Roll
}

// RPC Callback for Cartesian Coordinates (Hardware Abstraction Layer)
void receive_cartesian(float x, float y, float z, float pitch, float gripper_width, int duration_ms) {
  int raw[6];
  ik_map(x, y, z, pitch, gripper_width, raw);
  set_target_joints(raw[0], raw[1], raw[2], raw[3], raw[4], raw[5], duration_ms);
}

// Bypasses smoothing for fluid Cartesian paths
void stream_cartesian(float x, float y, float z, float pitch, float gripper_width) {
  int raw[6];
  ik_map(x, y, z, pitch, gripper_width, raw);
  stream_waypoints(raw[0], raw[1], raw[2], raw[3], raw[4], raw[5]);
}

// Disables torque on all servos (Follower Mode)
void freeze_arm() {
  Serial.println("FREEZE");
  for(int i=0; i<NUM_JOINTS; i++) joints[i].active = false;
}

// RPC Test Callback
int ping_arm() {
  while(Serial.available()) Serial.read();
  Serial.println("PING");
  unsigned long start = millis();
  while (millis() - start < 1000) {
    if (Serial.available()) {
      String response = Serial.readStringUntil('\n');
      response.trim();
      if (response == "PONG") return 1;
    }
  }
  return 0;
}

void setup() {
  Serial.begin(ARM_BAUD_RATE);
  for (int i = 0; i < NUM_JOINTS; i++) {
    joints[i].current_pos = home_pos[i];
    joints[i].start_pos = home_pos[i];
    joints[i].target_pos = home_pos[i];
    joints[i].duration = 3000.0;
    joints[i].elapsed = 3000.0;
    joints[i].active = false;
  }

  Bridge.begin(115200);
  Bridge.provide("receive_waypoints", receive_waypoints);
  Bridge.provide("receive_cartesian", receive_cartesian);
  Bridge.provide("stream_waypoints", stream_waypoints);
  Bridge.provide("stream_cartesian", stream_cartesian);
  Bridge.provide("freeze_arm", freeze_arm);
  Bridge.provide("ping_arm", ping_arm);

  delay(2000);
}

float minimum_jerk(float start, float target, float t) {
  if (t <= 0.0) return start;
  if (t >= 1.0) return target;
  float t3 = t * t * t;
  float t4 = t3 * t;
  float t5 = t4 * t;
  return start + (target - start) * (10.0f * t3 - 15.0f * t4 + 6.0f * t5);
}

unsigned long last_tick = 0;
void loop() {
  unsigned long now = millis();
  if (now - last_tick >= TICK_RATE_MS) {
    last_tick = now;
    for (int i = 0; i < NUM_JOINTS; i++) {
      if (joints[i].active) {
        joints[i].elapsed += TICK_RATE_MS;
        float t = joints[i].elapsed / joints[i].duration;
        if (t >= 1.0f) { t = 1.0f; joints[i].active = false; }
        joints[i].current_pos = minimum_jerk(joints[i].start_pos, joints[i].target_pos, t);
      }
    }
    Serial.print("<");
    for (int i = 0; i < NUM_JOINTS; i++) {
      Serial.print((int)joints[i].current_pos);
      if (i < NUM_JOINTS - 1) Serial.print(",");
    }
    Serial.println(">");
  }
}
