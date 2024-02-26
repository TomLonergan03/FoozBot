# Import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# Define the lower and upper boundaries of the "green" ball in the HSV color space
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# Initialize the list of tracked points
pts = deque(maxlen=args["buffer"])

# Load the template for edge detection and apply Canny to it
template_path = "/Users/arneshsaha/Desktop/FoozBot/vision/Images/TemplateNewCropped360x240.jpg"  # Change this to the correct path
temp = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
assert temp is not None, "Template file could not be read, check the path."
temp_edges = cv2.Canny(temp, 50, 200)
w, h = temp_edges.shape[::-1]

# Initialize VideoStream or VideoCapture
if not args.get("video", False):
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(args["video"])

time.sleep(2.0)  # Allow the camera or video file to warm up

# Function for Canny edge detection
def canny_edge(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 200)
    return edges

# Function to map ball position to normalized table coordinates
def map_to_normalized_coordinates(x, y, top_left, bottom_right):
    normalized_x = (x - top_left[0]) / (bottom_right[0] - top_left[0])
    normalized_y = (y - top_left[1]) / (bottom_right[1] - top_left[1])
    return normalized_x, normalized_y

# Main loop
while True:
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    if frame is None:
        break

    frame = imutils.resize(frame, width=600)
    edges_frame = canny_edge(frame)

    # Template matching to find the bounding box of the table
    res = cv2.matchTemplate(edges_frame, temp_edges, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

    # Detect and track the green ball
    mask = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), greenLower, greenUpper)
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
        
        # Map the ball's position to normalized coordinates
        if center:
            normalized_coords = map_to_normalized_coordinates(center[0], center[1], top_left, bottom_right)
            print(f"Ball's normalized coordinates: {normalized_coords}")
        
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    pts.appendleft(center)

    # Draw the trajectory of the ball
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # Display the frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

# Cleanup
if not args.get("video", False):
    vs.stop()
else:
    vs.release()
cv2.destroyAllWindows()
