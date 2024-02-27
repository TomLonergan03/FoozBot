# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
from PIL import Image

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (0, 134, 199)
greenUpper = (30, 255, 255)
pts = deque(maxlen=args["buffer"])

# Load the template for edge detection
temp_edges = cv2.imread("/Users/arneshsaha/Desktop/FoozBot/vision/Images/TemplateNewCropped360x240.jpg", cv2.IMREAD_GRAYSCALE)
assert temp_edges is not None, "file could not be read, check with os.path.exists()"
w, h = temp_edges.shape[::-1]

def canny_edge(frame):
    # Converting the frame to gray scale and applying Canny edge detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 198, 200, apertureSize=3, L2gradient=True)
    return blurred, edges

# Function to map ball position to normalized table coordinates
def map_to_normalized_coordinates(x, y, top_left, bottom_right):
    normalized_x = (x - top_left[0]) / (bottom_right[0] - top_left[0])
    normalized_y = (y - top_left[1]) / (bottom_right[1] - top_left[1])
    return normalized_x, normalized_y

# if a video path was not supplied, grab the reference to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
	# grab the current frame
	frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
	# Apply Canny edge detection and template matching
	frame = imutils.resize(frame, width=360, height=240)
	blurred_frame, edges_frame = canny_edge(frame)
	res = cv2.matchTemplate(edges_frame, temp_edges, cv2.TM_CCORR_NORMED)
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	top_left = max_loc # Using max_loc for CCoRR
	bottom_right = (top_left[0] + w - 5, top_left[1] + h - 5)
	cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)

	# Tracking green ball
	mask = cv2.inRange(cv2.cvtColor(cv2.GaussianBlur(imutils.resize(frame, width=360, height=240), (11, 11), 0), cv2.COLOR_BGR2HSV), greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	cnts = imutils.grab_contours(cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
	center = None
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		# When the ball is detected, draw a circle around it and a line tracing its path
		# Also, print the normalized coordinates of the ball with respect to the table
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			normalized_coords = map_to_normalized_coordinates(center[0], center[1], top_left, bottom_right)
			print("Ball's normalised coordinates",normalized_coords)
   
	pts.appendleft(center)
	for i in range(1, len(pts)):
		if pts[i - 1] is None or pts[i] is None:
			continue
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# Show the frame and the edges
	cv2.imshow("Frame", frame)
	cv2.imshow('Canny Edge Detection', edges_frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

# Cleanup
if not args.get("video", False):
	vs.stop()
else:
	vs.release()
cv2.destroyAllWindows()
