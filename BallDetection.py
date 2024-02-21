# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time

# Initialize global variables
ornageLower = (0, 134, 199)
ornageUpper = (30, 255, 255)
buffer_size = 64
pts = deque(maxlen=buffer_size)

def get_ball_center():
    # if a video path was not supplied, grab the reference
    # to the webcam
    vs = VideoStream(src=0).start()
    # allow the camera or video file to warm up
    time.sleep(2.0)
    # grab the current frame
    frame = vs.read()
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if False else frame
    # if we did not grab a frame, then we have reached the end of the video
    if frame is None:
        vs.stop()
        return None
    # Process the frame
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    vs.stop()  # Stop the video stream
    return center

if __name__ == "__main__":
    while True:
        center = get_ball_center()
        print(center)
        if center:
            # Here you could add your code to act on the center value
            pass
        time.sleep(1)  # Delay to limit the number of reads
