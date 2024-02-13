from trajectory import *
import numpy as np
import cv2

KNOWN_LOCATIONS = [Location(110, 120, 1),
                   Location(120, 125, 2),
                   Location(130, 130, 3),
                   Location(140, 132, 4),
                   Location(150, 134, 5),
                   Location(160, 135, 6),
                   Location(170, 130, 7),
                   Location(180, 125, 8),
                   Location(190, 130, 9),
                   Location(200, 135, 10),
                   Location(200, 140, 11),
                   Location(200, 145, 12),]

predictor = KalmanPredictor()
for i in range(len(KNOWN_LOCATIONS)):
    img = np.zeros((480, 480, 3), np.uint8)
    cv2.rectangle(img, (100, 100), (300, 300), (220, 0, 0), 3)
    for j in range(i):
        cv2.circle(img, (int(KNOWN_LOCATIONS[j].x), int(KNOWN_LOCATIONS[j].y)),
                   4, (0, 220, 20), -1)
    prediction = predictor.update(KNOWN_LOCATIONS[i])
    for loc in prediction.locations:
        cv2.circle(img, (int(loc.x), int(loc.y)),
                   4, (0, 20, 220), -1)
    cv2.imshow("Prediction", img)
    cv2.waitKey(0)
