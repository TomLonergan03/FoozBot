import cv2
import numpy as np

def nothing(x):
    pass

# Start capturing video
vid = cv2.VideoCapture(0)

cv2.namedWindow('Settings')
cv2.createTrackbar('Lower Hue', 'Settings', 20, 179, nothing)
cv2.createTrackbar('Upper Hue', 'Settings', 30, 179, nothing)

try:
    while(True):
        # Capture frame-by-frame
        ret, frame = vid.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert the captured frame from BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get the current positions of the trackbars
        lower_hue = cv2.getTrackbarPos('Lower Hue', 'Settings')
        upper_hue = cv2.getTrackbarPos('Upper Hue', 'Settings')

        lower_yellow = np.array([lower_hue, 100, 100])
        upper_yellow = np.array([upper_hue, 255, 255])

        # Threshold the HSV image to get only yellow colors
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        # Apply Gaussian Blur to reduce noise
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Loop over the contours
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Filter based on area
                # Approximate the contour
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                # Find the bounding box of the contour
                x, y, w, h = cv2.boundingRect(approx)
                # Draw the bounding box on the original frame
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the original frame with bounding box
        cv2.imshow('frame with bounding box', frame)

        # Break the loop with the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # When everything done, release the capture and destroy all windows
    vid.release()
    cv2.destroyAllWindows()
