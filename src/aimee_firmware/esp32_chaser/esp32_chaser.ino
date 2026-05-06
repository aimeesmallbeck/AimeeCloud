/**
 * ESP32 "Chaser" Firmware for ROArm-M3
 * Phase 5 of the AimeeCloud Dual-Core Pipeline.
 * 
 * Listens on UART0 (Serial) at 921600 baud for high-frequency 
 * micro-waypoints (<J1,J2,J3,J4,J5,J6>) from the STM32 co-processor.
 * Immediately pushes these to the ST3215 serial bus servos using SyncWrite 
 * to achieve fluid, jitter-free motion.
 */

#include <SCServo.h>

SMS_STS st;

// RoArm-M3 Servo IDs
#define BASE_ID             11
#define SHOULDER_DRIVING_ID 12
#define SHOULDER_DRIVEN_ID  13
#define ELBOW_ID            14
#define WRIST_ID            15
#define ROLL_ID             16
#define GRIPPER_ID          17

// Servo Serial Pins on Waveshare ESP32
#define S_RXD 18
#define S_TXD 19

uint8_t servo_ids[7] = {
  BASE_ID,
  SHOULDER_DRIVING_ID,
  SHOULDER_DRIVEN_ID,
  ELBOW_ID,
  WRIST_ID,
  ROLL_ID,
  GRIPPER_ID
};

int16_t servo_positions[7];
uint16_t servo_speeds[7] = {0, 0, 0, 0, 0, 0, 0}; // 0 = maximum speed (let STM32 handle trajectory timing)
uint8_t servo_accs[7]    = {0, 0, 0, 0, 0, 0, 0}; // 0 = maximum acceleration

void setup() {
  // Host communication (from STM32)
  Serial.begin(921600);
  
  // Servo communication (ST3215 bus runs at 1,000,000 baud)
  Serial1.begin(1000000, SERIAL_8N1, S_RXD, S_TXD);
  st.pSerial = &Serial1;
  
  while(!Serial) {}
  
  // Wait for servos to power up
  delay(1000);
  Serial.println("ESP32 Chaser Firmware Ready");
}

void loop() {
  // Expecting format: <J1,J2,J3,J4,J5,J6> or PING
  // J2 controls both SHOULDER_DRIVING and SHOULDER_DRIVEN (inverted)
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    
    if (input == "PING") {
      Serial.println("PONG");
    } else if (input.startsWith("<") && input.endsWith(">")) {
      // Remove brackets
      input = input.substring(1, input.length() - 1);
      
      int values[6];
      int count = 0;
      int startIdx = 0;
      int commaIdx;
      
      while ((commaIdx = input.indexOf(',', startIdx)) != -1 && count < 6) {
        values[count++] = input.substring(startIdx, commaIdx).toInt();
        startIdx = commaIdx + 1;
      }
      if (count < 6) {
        values[count++] = input.substring(startIdx).toInt();
      }
      
      if (count == 6) {
        // Map J1-J6 to the 7 servos
        servo_positions[0] = values[0];                 // Base
        servo_positions[1] = values[1];                 // Shoulder driving
        servo_positions[2] = 4095 - values[1];          // Shoulder driven (mechanically inverted)
        servo_positions[3] = values[2];                 // Elbow
        servo_positions[4] = values[3];                 // Wrist
        servo_positions[5] = values[4];                 // Roll
        servo_positions[6] = values[5];                 // Gripper
        
        // Execute synchronous write
        st.SyncWritePosEx(servo_ids, 7, servo_positions, servo_speeds, servo_accs);
      }
    }
  }
}
