import cv2
import numpy as np
from PIL import Image

global_start_coords = (0.0, 0.0)
global_end_coords = (100.0, 100.0)
global_ball_coords = (50.0, 50.0)

temp_edges = cv2.imread("vision\Images\TemplateCropped360x240.jpg", cv2.IMREAD_GRAYSCALE)
assert temp_edges is not None, "file could not be read, check with os.path.exists()"


def canny_edge(frame):
    # Converting the frame to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 130, 150)
    return blurred, edges

def getBallCoordsInPercent():
    return __calcCoordsInPercent(global_ball_coords)

def __calcCoordsInPercent(coords):
    coords_max = (global_end_coords[0] - global_start_coords[0], global_end_coords[1] - global_start_coords[1])
    return ((coords[0] / coords_max[0], coords[1] / coords_max[1]))

def getGlobalStartCoords():
    return global_start_coords

def getGlobalEndCoords():
    return global_end_coords

def getGlobaLBalCoords():
    return global_ball_coords

def setGlobalBallCoords(coords):
    global_ball_coords = coords
    
#_, temp_edges = canny_edge(template)
#temp_edges = cv2.resize(temp_edges, (640, 480))
#cv2.imwrite("TemplateEdges.jpg", temp_edges)
w, h = temp_edges.shape[::-1]

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 360)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 10)
while True:
    ret, frame = cap.read(cv2.IMREAD_GRAYSCALE)
    blurred, edges = canny_edge(frame)

    res = cv2.matchTemplate(edges, temp_edges, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc # Using max_loc for CCoRR
    global_start_coords = tuple(top_left)
    bottom_right = (top_left[0] + w - 5, top_left[1] + h - 5)
    global_end_coords = tuple(bottom_right)

    #cv2.rectangle(edges, top_left, bottom_right, 210, 2)
    # 640 480
    cv2.imshow('Canny Edge Detection', edges)
    cv2.imshow("Template Edges", temp_edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()