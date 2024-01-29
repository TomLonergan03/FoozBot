# This scripts does object detection on a live video feed from a webcam with the actual background

import cv2
import numpy as np

# Start capturing video
vid = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = vid.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert the captured frame from BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of yellow color in HSV
    # Adjust these values to better suit the yellow color you're detecting
    lower_yellow = np.array([20, 100, 100])  # Updated to more accurate yellow range
    upper_yellow = np.array([30, 255, 255])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours
    for contour in contours:
        # Approximate the contour
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        # Find the bounding box of the contour
        x, y, w, h = cv2.boundingRect(approx)
        # Draw the bounding box on the original frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the original frame with bounding box
    cv2.imshow('frame with bounding box', frame)

    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy all windows
vid.release()
cv2.destroyAllWindows()
