from collections import deque
import numpy as np
import cv2
import imutils
import time
from imutils.video import VideoStream
import argparse

# Initialize the list of argument parsers
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# Define the lower and upper boundaries of the "green" ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

# Attempt to grab the specific tracker using OpenCV's newer syntax
def create_tracker_by_name(tracker_type):
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    # You can add more trackers here
    else:
        tracker = None
    return tracker

# Load the template for edge detection (adjust the path as needed)
temp_edges = cv2.imread("/Users/arneshsaha/Desktop/FoozBot/vision/Images/TemplateNewCropped360x240.jpg", cv2.IMREAD_GRAYSCALE)
assert temp_edges is not None, "Template file could not be read, check the path."
w, h = temp_edges.shape[::-1]

# Initialize video stream or video file
if not args.get("video", False):
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(args["video"])
time.sleep(2.0)

first_detection = True
tracker = None

while True:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    if frame is None:
        break

    frame = imutils.resize(frame, width=600)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred_frame = cv2.GaussianBlur(gray_frame, (7, 7), 0)
    edges_frame = cv2.Canny(blurred_frame, 50, 150)

    if first_detection:
        res = cv2.matchTemplate(edges_frame, temp_edges, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        bbox = (top_left[0], top_left[1], w, h)
        
        tracker = create_tracker_by_name('KCF')
        if tracker is not None:
            tracker.init(frame, bbox)
            first_detection = False
    else:
        success, bbox = tracker.update(frame)
        if success:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

    # Ball tracking code (remains the same)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

if not args.get("video", False):
    vs.stop()
else:
    vs.release()
cv2.destroyAllWindows()
