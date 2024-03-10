from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import warnings
import os


class BallEdgeDetection():
    def __init__(self, src):
        self.greenLower = (0, 134, 199)
        self.greenUpper = (30, 255, 255)
        self.pts = deque(maxlen=10)

        # Load the template for edge detection
        self.temp_edges = cv2.imread("Images/TemplateNewCropped360x240.jpg", cv2.IMREAD_GRAYSCALE)
        assert self.temp_edges is not None, "file could not be read, check with os.path.exists()"
        w, h = self.temp_edges.shape[::-1]
        self.w = w
        self.h = h

        # if a video path was not supplied, grab the reference to the webcam
        self.vs = VideoStream(src=src).start()
        self.frame = self.vs.read()

        self.top_left_bottom_right = self.get_top_left_bottom_right()

        time.sleep(2.0)

    def get_ball_position(self):
        # grab the current frame
        self.frame = self.vs.read()
        # handle the frame from VideoCapture or VideoStream

        # frame = frame[1] if args.get("video", False) else frame

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if self.frame is None:
            return
        # Apply Canny edge detection and template matching
        self.frame = imutils.resize(self.frame, width=360, height=240)

        # Tracking green ball
        mask = cv2.inRange(
            cv2.cvtColor(cv2.GaussianBlur(imutils.resize(self.frame, width=360, height=240), (11, 11), 0),
                         cv2.COLOR_BGR2HSV),
            self.greenLower, self.greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = imutils.grab_contours(cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
        center = None

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            return
        return center

    def get_top_left_bottom_right(self):
        self.frame = self.vs.read()
        self.frame = imutils.resize(self.frame, width=360, height=240)
        blurred_frame, edges_frame = self.canny_edge(self.frame)
        res = cv2.matchTemplate(edges_frame, self.temp_edges, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc  # Using max_loc for CCoRR
        bottom_right = (top_left[0] + self.w - 5, top_left[1] + self.h - 5)


        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            return
        return (top_left, bottom_right)

    def canny_edge(self, frame):
        # Converting the frame to gray scale and applying Canny edge detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 130, 150)
        return blurred, edges

    def get_frame(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=360, height=240)

        # DISPLAY BOARD
        top_left = self.top_left_bottom_right[0]
        bottom_right = self.top_left_bottom_right[1]
        cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)

        # DISPLAY TRAIL
        centre = self.get_ball_position()
        self.pts.appendleft(centre)
        for i in range(1, len(self.pts)):
            if self.pts[i - 1] is None or self.pts[i] is None:
                continue
            thickness = int(np.sqrt(10 / float(i + 1)) * 2.5)
            cv2.line(frame, self.pts[i - 1], self.pts[i], (0, 0, 255), thickness)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            return

        return frame
