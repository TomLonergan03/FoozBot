import cv2
import numpy as np

# Function to filter based on area and aspect ratio
def filter_contour(contour, min_area=100, aspect_ratio_range=(0.5, 1.5)):
    _, _, w, h = cv2.boundingRect(contour)
    area = cv2.contourArea(contour)
    aspect_ratio = float(w)/h if h > 0 else 0

    if area > min_area and aspect_ratio_range[0] < aspect_ratio < aspect_ratio_range[1]:
        return True
    return False

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

    # Updated HSV range for yellow (tweak these values as needed)
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Apply Gaussian blur to the mask to reduce noise
    blurred_mask = cv2.GaussianBlur(mask, (9, 9), 0)

    # Use morphological operations to remove small objects and fill small holes
    # Erode followed by dilate (opening operation)
    mask_opened = cv2.morphologyEx(blurred_mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    # Find contours in the processed mask
    contours, _ = cv2.findContours(mask_opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours
    for contour in contours:
        if filter_contour(contour):
            # Calculate the bounding box of the contour and draw it
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the original frame with bounding box
    cv2.imshow('frame with bounding box', frame)

    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy all windows
vid.release()
cv2.destroyAllWindows()
