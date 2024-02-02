import cv2
import numpy as np

def detect_table_edges(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise and help edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny edge detector to find edges
    edges = cv2.Canny(blurred, 50, 150)

    # Use HoughLinesP to detect lines in the edge image
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    # Draw the detected lines on the original frame
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return frame

# Capture video from the default camera (you can change the argument to use a different camera)
cap = cv2.VideoCapture(1)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    # Perform table edge detection and draw lines
    result_frame = detect_table_edges(frame)

    # Display the result
    cv2.imshow('Table Edge Detection', result_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
