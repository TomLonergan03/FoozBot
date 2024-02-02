import cv2
import numpy as np

def canny_edge(frame):
    # Converting the frame to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 130, 150)
    return edges

cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    blurred,edges = canny_edge(frame)
    cv2.imshow('Canny Edge Detection', edges)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()