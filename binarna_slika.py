import cv2
import numpy as np
import os


def binary_image(image):
    
    
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Yellow color boundaries
    yellow_boundaries = {
        "lower": np.array([18, 94, 140]),  
        "upper": np.array([48, 255, 255]) 
    }

    # White color boundaries
    white_boundaries = {
        "lower": np.array([0, 0, 200]),  
        "upper": np.array([255, 25, 255])  
    }


    yellow_mask = cv2.inRange(hsv_image, yellow_boundaries["lower"], yellow_boundaries["upper"])
    white_mask = cv2.inRange(hsv_image, white_boundaries["lower"], white_boundaries["upper"])
    combined_mask = cv2.bitwise_or(yellow_mask, white_mask)


    # Remove noise with Gaussian blur
    smooth_image = cv2.GaussianBlur(combined_mask, (7, 7), 0)

    # Edge detection using Canny
    detected_edges = cv2.Canny(smooth_image, 30, 100)


    return detected_edges




