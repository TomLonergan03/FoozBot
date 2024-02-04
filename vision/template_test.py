import cv2
import numpy as np

# Start capturing video
vid = cv2.VideoCapture(2)
template = cv2.imread("vision\Images\TemplateFieldDetection.png", cv2.IMREAD_GRAYSCALE)
assert template is not None, "file could not be read, check with os.path.exists()"
#template = cv2.cvtColor(template, cv2.COLOR_BAYER_BG2GRAY)
w, h = template.shape[::-1]

while(True):
    # Capture frame-by-frame
    ret, frame = vid.read()
    if not ret:
        print("Failed to grab frame")

    # Convert the captured frame from BGR to Grayscale
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply template Matching
    res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc # Using max_loc for CCOEFF
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(frame, top_left, bottom_right, 255, 2)

    # Display the original frame with bounding box
    cv2.imshow('Template Detection', frame)

    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy all windows
vid.release()
cv2.destroyAllWindows()

