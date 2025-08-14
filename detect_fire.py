import cv2
import numpy as np

def detect_fire_from_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV ranges for fire colors
    lower_red = np.array([0, 50, 50], dtype="uint8")
    upper_red = np.array([10, 255, 255], dtype="uint8")

    lower_orange = np.array([11, 50, 50], dtype="uint8")
    upper_orange = np.array([25, 255, 255], dtype="uint8")

    lower_yellow = np.array([26, 50, 50], dtype="uint8")
    upper_yellow = np.array([35, 255, 255], dtype="uint8")

    # Create masks
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    combined_mask = cv2.bitwise_or(mask_red, mask_orange)
    combined_mask = cv2.bitwise_or(combined_mask, mask_yellow)

    fire_area = cv2.bitwise_and(image, image, mask=combined_mask)

    # Fire detection threshold
    fire_pixels = cv2.countNonZero(combined_mask)
    fire_detected = fire_pixels > 500

    return fire_detected, fire_area
