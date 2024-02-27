# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


class Vision():

    def __init__(self, ball_tail: int):
        self.vs = VideoStream(src=4).start()
        # pts = deque(maxlen=args["buffer"])
        self.ball_tail_length = ball_tail
        self.pts = deque(maxlen=ball_tail)
        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space, then initialize the
        # list of tracked points
        self.ballLower = (0, 134, 199)
        self.ballUpper = (30, 255, 255)

        # Input the edge detection here and pass into the lower 2 values
        self.topLeftCoord = (14, 30)
        # If hardcoding, find correct values
        self.bottomRightCoord = (500, 400)
        self.framesPassed = 0

    # construct the argument parse and parse the arguments
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
                    help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", type=int, default=64,
                    help="max buffer size")
    args = vars(ap.parse_args())

    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
        vs = VideoStream(src=0).start()
    # otherwise, grab a reference to the video file
    else:
        vs = cv2.VideoCapture(args["video"])
    # allow the camera or video file to warm up
    time.sleep(2.0)
    """

    def normalise_coords(self, coord_x: float, coord_y: float):
        """Takes input coordinates """
        temp_x = coord_x - self.topLeftCoord[0]
        temp_y = coord_y - self.topLeftCoord[1]
        return (temp_x, temp_y)

    def unnormalise_coords(self, coord_x: float, coord_y: float):
        """Reverse of normalise_coords. Takes normalised coordinates"""
        temp_x = coord_x + self.topLeftCoord[0]
        temp_y = coord_y + self.topLeftCoord[1]
        return (temp_x, temp_y)

    def get_frame(self):
        # grab the current frame
        frame = self.vs.read()
        # handle the frame from VideoCapture or VideoStream
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if frame is None:
            return
        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=640)
        return frame

    def get_ball_position(self):
        frame = self.get_frame()
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.ballLower, self.ballUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        # update the points queue
        self.pts.appendleft(center)

        # loop over the set of tracked points
        for i in range(1, len(self.pts)):
            # if either of the tracked points are None, ignore
            # them
            if self.pts[i - 1] is None or self.pts[i] is None:
                continue
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(
                np.sqrt(self.ball_tail_length / float(i + 1)) * 2.5)
            cv2.line(frame, self.pts[i - 1],
                     self.pts[i], (0, 0, 255), thickness)
        # show the frame to our screen
        # cv2.imshow("Frame", frame)
        # key = cv2.waitKey(1) & 0xFF

        self.framesPassed += 1
        return self.normalise_coords(*(x, y)), self.framesPassed, frame

    def edge_detection():
        # Do Edge detection
        return

    def update(self):
        return self.get_ball_position(), self.normalise_coords(*self.bottomRightCoord)
