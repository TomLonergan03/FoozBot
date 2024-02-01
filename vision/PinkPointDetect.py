# Detects Pink Points very well!!
import cv2
import numpy as np
from itertools import combinations

def detect_and_draw_lines(frame):
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for pink color in HSV
    lower_pink = np.array([158, 49, 208])
    upper_pink = np.array([194, 255, 255])

    # Create a binary mask using inRange function to detect pink color
    mask = cv2.inRange(hsv, lower_pink, upper_pink)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw pink contours on the original frame
    cv2.drawContours(frame, contours, -1, (255, 182, 193), 2)

    # Draw straight lines between pink points
    for contour in contours:
        # Extract pink points (contour points)
        pink_points = contour.reshape(-1, 2)

        # Iterate over all combinations of pink points
        for point1, point2 in combinations(pink_points, 2):
            point1 = tuple(point1)
            point2 = tuple(point2)

            # Draw a line connecting the pink points
            cv2.line(frame, point1, point2, (0, 255, 0), 2)

    return frame

# Capture video from the default camera (you can change the argument to use a different camera)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    # Perform pink color detection and draw lines between pink points
    result_frame = detect_and_draw_lines(frame)

    # Display the result
    cv2.imshow('Pink Color Detection and Line Drawing', result_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
