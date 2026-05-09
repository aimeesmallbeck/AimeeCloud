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
uint16_t servo_speeds[7] = {0, 0, 0, 0, 0, 0, 0}; 
uint8_t servo_accs[7]    = {0, 0, 0, 0, 0, 0, 0}; 

int shoulder_offset = 0;
bool is_calibrated = false;

void setup() {
  Serial.begin(921600);
  
  Serial1.begin(1000000, SERIAL_8N1, S_RXD, S_TXD);
  st.pSerial = &Serial1;
  
  while(!Serial) {}
  delay(1000);

  // Attempt initial calibration. 
  int driving_pos = st.ReadPos(SHOULDER_DRIVING_ID);
  int driven_pos = st.ReadPos(SHOULDER_DRIVEN_ID);
  
  if (driving_pos != -1 && driven_pos != -1) {
      shoulder_offset = 4095 - (driving_pos + driven_pos);
      is_calibrated = true;
  }

  Serial.println("ESP32 Chaser Firmware Ready");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    
    if (input == "PING") {
      Serial.println("PONG");
    } else if (input == "FREEZE") {
      for(int i=0; i<7; i++) st.EnableTorque(servo_ids[i], 0);
      Serial.println("FROZEN");
    } else if (input == "READ") {
      Serial.print("POS:<");
      for(int i=0; i<7; i++) {
        int pos = st.ReadPos(servo_ids[i]);
        if (pos != -1) Serial.print(pos);
        else Serial.print("ERR");
        if (i < 6) Serial.print(",");
      }
      Serial.println(">");
    } else if (input.length() > 5 && input.startsWith("<") && input.endsWith(">")) {
      
      // LAZY CALIBRATION: Fix offset if 12V was off at boot
      if (!is_calibrated) {
        int driving_pos = st.ReadPos(SHOULDER_DRIVING_ID);
        int driven_pos = st.ReadPos(SHOULDER_DRIVEN_ID);
        if (driving_pos != -1 && driven_pos != -1) {
            shoulder_offset = 4095 - (driving_pos + driven_pos);
            is_calibrated = true;
        }
      }

      input = input.substring(1, input.length() - 1);
      
      int values[6];
      int count = 0;
      int startIdx = 0;
      int commaIdx;
      
      while ((commaIdx = input.indexOf(',', startIdx)) != -1 && count < 6) {
        values[count++] = input.substring(startIdx, commaIdx).toInt();
        startIdx = commaIdx + 1;
      }
      if (count < 6) values[count++] = input.substring(startIdx).toInt();
      
      // Strict validation: Only execute if exactly 6 valid ints were parsed
      // and they are within absolute physical bounds
      if (count == 6 && values[0] > 0 && values[0] < 4096) {
        servo_positions[0] = values[0];                 
        servo_positions[1] = values[1];                 
        
        // Prevent math underflow on driven shoulder
        int inverted = (4095 - values[1]) - shoulder_offset;
        if (inverted < 0) inverted = 0;
        if (inverted > 4095) inverted = 4095;
        servo_positions[2] = inverted; 
        
        servo_positions[3] = values[2];                 
        servo_positions[4] = values[3];                 
        servo_positions[5] = values[4];                 
        servo_positions[6] = values[5];                 
        
        st.SyncWritePosEx(servo_ids, 7, servo_positions, servo_speeds, servo_accs);
      }
    }
  }
}
