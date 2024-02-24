import cv2
import numpy as np

def find_foosball_table(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise and help edge detection
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Invert the colors
    thresh = cv2.bitwise_not(thresh)
    
    # Find contours in the edges
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by area
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]
    
    if contours:
        # Find the contour with the maximum area (assumed to be the foosball table)
        max_contour = max(contours, key=cv2.contourArea)
        
        # Approximate the contour as a rectangle
        epsilon = 0.02 * cv2.arcLength(max_contour, True)
        approx = cv2.approxPolyDP(max_contour, epsilon, True)
        
        # Draw a boundary around the foosball table
        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
        
        # Draw circles at the corner coordinates
        for point in approx:
            cv2.circle(frame, tuple(point[0]), 5, (255, 0, 0), -1)
    
    return frame

# Capture video from the default camera (you can change the argument to use a different camera)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()
    
    # Perform foosball table detection
    result_frame = find_foosball_table(frame)
    
    # Display the result
    cv2.imshow('Foosball Table Detection', result_frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
