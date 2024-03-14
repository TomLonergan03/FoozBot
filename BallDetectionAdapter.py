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
        self.ballLower = (0, 134, 199)
        self.ballUpper = (30, 255, 255)
        self.pts = deque(maxlen=10)

        self.playersLower = (35, 80, 156)
        self.playersUpper = (172, 184, 255)
        # Load the template for edge detection
        self.temp_edges = cv2.imread("Images/TemplateNewCropped360x240.jpg", cv2.IMREAD_GRAYSCALE)
        assert self.temp_edges is not None, "file could not be read, check with os.path.exists()"
        w, h = self.temp_edges.shape[::-1]
        self.w = w
        self.h = h

        # if a video path was not supplied, grab the reference to the webcam
        self.vs = VideoStream(src=src).start()
        self.frame = self.vs.read()
        self.frame_no = 0
        # self.frame_num = 0

        self.top_left_bottom_right = self.get_top_left_bottom_right()

        time.sleep(2.0)

    def get_ball_position(self):
        # grab the current frame
        self.frame = self.vs.read()
        self.frame_no += 1
        # self.frame_num += 1
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
            self.ballLower, self.ballUpper)
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
        _, edges_frame = self.canny_edge(self.frame)
        res = cv2.matchTemplate(edges_frame, self.temp_edges, cv2.TM_CCORR_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(res)
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

    def get_players_x(self):
        self.frame = self.vs.read()
        if self.frame is None:
            return

        self.frame = imutils.resize(self.frame, width=360, height=240)
        outp_x = []
        outp_y = []

        mask = cv2.inRange(
            cv2.cvtColor(cv2.GaussianBlur(self.frame, (11, 11), 0),
                         cv2.COLOR_BGR2HSV),
            self.playersLower, self.playersUpper)
        # mask = cv2.erode(mask, None, iterations=2)
        # mask = cv2.dilate(mask, None, iterations=2)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=1)

        cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            # cv2.rectangle(self.frame, (x, y), (x + w, y + h), (36,255,12), 2)
            outp_x.append(x + w/2)
            outp_y.append(y + h/2)
        
        # cv2.imshow('mask', mask)
        # cv2.imshow('close', close)
        # cv2.imshow('frame', self.frame)
        return outp_x, outp_y

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

        #key = cv2.waitKey(1) & 0xFF
        #if key == ord("q"):
        #    return

        return frame
