import cv2
import numpy as np
from PIL import Image

temp_edges = cv2.imread("vision\Images\TemplateCropped.jpg", cv2.IMREAD_GRAYSCALE)
assert temp_edges is not None, "file could not be read, check with os.path.exists()"

def canny_edge(frame):
    # Converting the frame to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 130, 150)
    return blurred, edges

#_, temp_edges = canny_edge(template)
#temp_edges = cv2.resize(temp_edges, (640, 480))
#cv2.imwrite("TemplateEdges.jpg", temp_edges)
w, h = temp_edges.shape[::-1]

cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read(cv2.IMREAD_GRAYSCALE)
    blurred, edges = canny_edge(frame)

    res = cv2.matchTemplate(edges, temp_edges, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc # Using max_loc for CCoRR
    bottom_right = (top_left[0] + w - 5, top_left[1] + h - 5)

    cv2.rectangle(edges, top_left, bottom_right, (255, 0, 0), 2)
    # 640 480
    cv2.imshow('Canny Edge Detection', edges)
    cv2.imshow("Template Edges", temp_edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()