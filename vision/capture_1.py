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
    # These values can be adjusted depending on the shade of yellow you want to detect
    lower_yellow = np.array([204, 139, 90])
    upper_yellow = np.array([239, 166, 109])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Bitwise-AND mask and original image to get the yellow parts of the image
    yellow_detection = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the original frame and the yellow detection output
    cv2.imshow('frame', frame)
    cv2.imshow('yellow detection', yellow_detection)

    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy all windows
vid.release()
cv2.destroyAllWindows()
