/**
 * STM32U585 "Real-Time Trajectory Engine" Firmware
 * Phase 4 of the AimeeCloud Dual-Core Pipeline.
 * 
 * Runs on the UNO Q's STM32 co-processor.
 * Uses Arduino_RouterBridge to receive RPC commands from the ARM64.
 * Computes a smooth minimum-jerk (quintic) trajectory.
 * Streams micro-waypoints at 50Hz (20ms) to the ESP32 via Hardware Serial.
 */

#include <Arduino.h>
#include <bridge.h>

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

// For simplicity, we initialize at a home position (approximate middle for 12-bit servos)
int home_pos = 2047;

// RPC Callback
void receive_waypoints(int j1, int j2, int j3, int j4, int j5, int j6, int duration_ms) {
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

// RPC Test Callback
int ping_arm() {
  // Clear buffer
  while(Serial.available()) Serial.read();
  
  // Send ping
  Serial.println("PING");
  
  // Wait for reply
  unsigned long start = millis();
  while (millis() - start < 1000) {
    if (Serial.available()) {
      String response = Serial.readStringUntil('\n');
      response.trim();
      if (response == "PONG") {
        return 1; // Success
      }
    }
  }
  return 0; // Timeout
}

void setup() {
  // Communication with ESP32 (Using Serial - external TX/RX pins D0 and D1)
  Serial.begin(ARM_BAUD_RATE);
  
  for (int i = 0; i < NUM_JOINTS; i++) {
    joints[i].current_pos = home_pos;
    joints[i].start_pos = home_pos;
    joints[i].target_pos = home_pos;
    joints[i].duration = 0;
    joints[i].elapsed = 0;
    joints[i].active = false;
  }

  // Initialize RPC Bridge to ARM64 (Zephyr thread starts automatically in background on Serial1)
  Bridge.begin(115200);
  Bridge.provide("receive_waypoints", receive_waypoints);
  Bridge.provide("ping_arm", ping_arm);
}

// Minimum Jerk Trajectory (Quintic Polynomial)
// Returns interpolated position given t in [0, 1]
float minimum_jerk(float start, float target, float t) {
  if (t <= 0.0) return start;
  if (t >= 1.0) return target;
  float t3 = t * t * t;
  float t4 = t3 * t;
  float t5 = t4 * t;
  // 10t^3 - 15t^4 + 6t^5
  float scale = 10.0f * t3 - 15.0f * t4 + 6.0f * t5;
  return start + (target - start) * scale;
}

unsigned long last_tick = 0;

void loop() {
  // Real-Time Trajectory Generation (50Hz)
  // Note: RPC parsing happens asynchronously in the Zephyr 'bridge' thread
  unsigned long now = millis();
  if (now - last_tick >= TICK_RATE_MS) {
    last_tick = now;
    bool moving = false;
    
    for (int i = 0; i < NUM_JOINTS; i++) {
      if (joints[i].active) {
        moving = true;
        joints[i].elapsed += TICK_RATE_MS;
        float t = joints[i].elapsed / joints[i].duration;
        
        if (t >= 1.0f) {
          t = 1.0f;
          joints[i].active = false; // Reached target
        }
        
        joints[i].current_pos = minimum_jerk(joints[i].start_pos, joints[i].target_pos, t);
      }
    }
    
    // Send Micro-waypoints to ESP32
    // Send even if not actively moving to ensure servos hold position
    Serial.print("<");
    for (int i = 0; i < NUM_JOINTS; i++) {
      Serial.print((int)joints[i].current_pos);
      if (i < NUM_JOINTS - 1) Serial.print(",");
    }
    Serial.println(">");
  }
}
