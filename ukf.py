from filterpy.kalman import UnscentedKalmanFilter as UKF
from filterpy.kalman import ExtendedKalmanFilter as EKF
from filterpy.kalman import MerweScaledSigmaPoints
import numpy as np
import cv2

path = UKF(2, 2, dt=0.1, hx=lambda x: x, fx=lambda x,
           dt: x, points=MerweScaledSigmaPoints(2, kappa=1.0, alpha=1e-3, beta=2.0))
path.x = np.array([0, 0])
path.P *= 0.1
path.R *= 5
path.Q *= 0.1
path.H = np.array([[1, 0], [0, 1]])
path.F = np.array([[1, 1], [0, 1]])
path.B = np.array([[0.5, 0.5], [0.5, 0.5]])

img = np.zeros((480, 480, 3), np.uint8)
for i in range(0, 480, 10):
    cv2.circle(img, (i, i*i//100), 4, (0, 220, 20), -1)
    path.predict()
    path.update(np.array([i, i*i//100]))
    cv2.circle(img, (int(path.x[0]), int(path.x[1])), 4, (0, 20, 220), 1)

cv2.imshow("Prediction", img)
cv2.waitKey(0)

path = EKF(2, 2)
path.x = np.array([0, 0])
path.P *= 0.1
path.R *= 5
path.Q *= 0.1
path.H = np.array([[1, 0], [0, 1]])
path.F = np.array([[1, 1], [0, 1]])
path.B = np.array([[0.5, 0.5], [0.5, 0.5]])

img = np.zeros((480, 480, 3), np.uint8)
for i in range(0, 480, 10):
    cv2.circle(img, (i, i*i//100), 4, (0, 220, 20), -1)
    path.predict()
    path.update(np.array([i, i*i//100]), lambda x: x, lambda x: x)
    print(path.x)
    cv2.circle(img, (int(path.x[0]), int(path.x[1])), 4, (0, 20, 220), 1)

cv2.imshow("Prediction", img)
cv2.waitKey(0)
