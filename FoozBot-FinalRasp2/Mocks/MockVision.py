import math
from collections import deque
import cv2
from imutils.video import VideoStream
import imutils
import numpy as np


class MockVision:
    def __init__(self):
        self.counter = 0
        self.travel_speed = 0.005

    def get_ball_position(self):
        self.counter += 1

        x = self.circle_x + math.cos(self.counter * self.travel_speed)
        y = self.cirlce_y + math.sin(self.counter * self.travel_speed)

        return (x,y), self.counter

    def get_bottom_right(self):
        return 0, 0



# Your initialization code
vs = VideoStream(src=0).start()
ball_tail = 10  # Replace with your desired value
ball_tail_length = ball_tail
pts = deque(maxlen=ball_tail)
ballLower = (0, 134, 199)
ballUpper = (30, 255, 255)
topLeftCoord = (14, 30)
bottomRightCoord = (500, 400)
framesPassed = 0

temp_edges = cv2.imread("../Images/TemplateNewCropped360x240.jpg", cv2.IMREAD_GRAYSCALE)
(w, h) = temp_edges.shape[:2]
w = w
h = h

while True:
    # Retrieve a frame from the video stream
    frame = vs.read()

    # Check if the frame is None (end of the video stream)
    if frame is None:
        break

    # Your existing processing code...
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, ballLower, ballUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # ... (the rest of your processing code)

    # Show the frame to the screen
    cv2.imshow("Frame", frame)

    # Wait for a key event (with a delay)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoStream and close all windows
vs.stop()
cv2.destroyAllWindows()