# Draws lines between two detected pink points
import cv2
import numpy as np

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

    # Find the centroid of each contour (pink point)
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)

    # Draw straight lines connecting the pink points
    if len(contours) >= 2:
        for i in range(len(contours) - 1):
            M1 = cv2.moments(contours[i])
            M2 = cv2.moments(contours[i + 1])

            if M1["m00"] != 0 and M2["m00"] != 0:
                cx1 = int(M1["m10"] / M1["m00"])
                cy1 = int(M1["m01"] / M1["m00"])

                cx2 = int(M2["m10"] / M2["m00"])
                cy2 = int(M2["m01"] / M2["m00"])

                cv2.line(frame, (cx1, cy1), (cx2, cy2), (0, 255, 0), 2)

    return frame

# Capture video from the default camera (you can change the argument to use a different camera)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    # Perform pink color detection and draw lines
    result_frame = detect_and_draw_lines(frame)

    # Display the result
    cv2.imshow('Pink Color Detection and Line Drawing', result_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
