import cv2
import numpy as np
import sys

def detect_dice(image_path):
    cv_image = cv2.imread(image_path)
    if cv_image is None:
        print(f"ERROR: Could not read {image_path}")
        return
        
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    
    # Red ranges (very relaxed)
    lower_red1 = np.array([0, 50, 40])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([160, 50, 40])
    upper_red2 = np.array([180, 255, 255])
    
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    # Clean up mask
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_cnt = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_cnt)
        if area > 20:
            M = cv2.moments(largest_cnt)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                print(f"DETECTED:{cx},{cy}")
                # Save debug image
                cv2.drawContours(cv_image, [largest_cnt], -1, (0, 255, 0), 2)
                cv2.circle(cv_image, (cx, cy), 5, (255, 0, 0), -1)
                cv2.imwrite('/workspace/test_detection_result.jpg', cv_image)
                return
    print("NOT_DETECTED")

if __name__ == '__main__':
    detect_dice('/workspace/dice_pick_frame.jpg')
