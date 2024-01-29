import cv2
import numpy as np

def nothing(x):
    pass

# Create a window
cv2.namedWindow('HSV Adjustments')
cv2.createTrackbar('Lower H', 'HSV Adjustments', 0, 179, nothing)
cv2.createTrackbar('Lower S', 'HSV Adjustments', 100, 255, nothing)
cv2.createTrackbar('Lower V', 'HSV Adjustments', 100, 255, nothing)
cv2.createTrackbar('Upper H', 'HSV Adjustments', 179, 179, nothing)
cv2.createTrackbar('Upper S', 'HSV Adjustments', 255, 255, nothing)
cv2.createTrackbar('Upper V', 'HSV Adjustments', 255, 255, nothing)

vid = cv2.VideoCapture(0)

while True:
    _, frame = vid.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get slider positions
    lh = cv2.getTrackbarPos('Lower H', 'HSV Adjustments')
    ls = cv2.getTrackbarPos('Lower S', 'HSV Adjustments')
    lv = cv2.getTrackbarPos('Lower V', 'HSV Adjustments')
    uh = cv2.getTrackbarPos('Upper H', 'HSV Adjustments')
    us = cv2.getTrackbarPos('Upper S', 'HSV Adjustments')
    uv = cv2.getTrackbarPos('Upper V', 'HSV Adjustments')

    # Define HSV range based on sliders
    lower_hsv = np.array([lh, ls, lv])
    upper_hsv = np.array([uh, us, uv])

    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    cv2.imshow('result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
