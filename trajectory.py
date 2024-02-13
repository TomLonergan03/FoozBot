from collections import deque
from dataclasses import dataclass

import numpy as np
import cv2


@dataclass
class Location:
    x: float
    y: float
    time: float


@dataclass
class Trajectory:
    locations: [Location]


class NaivePredictor:
    def __init__(self, board_x: int = 200, board_y: int = 200):
        self.history = deque(maxlen=2)
        self.history.append(Location(0, 0, 0))
        self.board_x = board_x
        self.board_y = board_y

    def update(self, location: Location) -> Trajectory:
        self.history.append(location)
        future = [self.calculateFutureLocation(
            self.history, 1) for _ in range(1, 50)]
        return Trajectory(future)

    def calculateFutureLocation(self, trajectory: Trajectory, time: float) -> Location:
        dx = (trajectory[1].x - trajectory[0].x) / \
            (trajectory[1].time - trajectory[0].time)
        dy = (trajectory[1].y - trajectory[0].y) / \
            (trajectory[1].time - trajectory[0].time)
        if trajectory[1].x >= 300 or trajectory[1].x <= 100:
            dx = -dx
        if trajectory[1].y >= 300 or trajectory[1].y <= 100:
            dy = -dy
        new_location = Location(
            trajectory[1].x + dx * time, trajectory[1].y + dy * time, trajectory[1].time + time)
        self.history.append(new_location)
        return new_location


class KalmanFilter:
    kf = cv2.KalmanFilter(4, 2)
    kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
    kf.transitionMatrix = np.array(
        [[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)

    def predict(self, coordX, coordY):
        ''' This function estimates the position of the object'''
        measured = np.array([[np.float32(coordX)], [np.float32(coordY)]])
        self.kf.correct(measured)
        predicted = self.kf.predict()
        x, y = int(predicted[0]), int(predicted[1])
        return x, y


class KalmanPredictor:
    def __init__(self, board_x: int = 200, board_y: int = 200):
        self.kf = KalmanFilter()
        self.board_x = board_x
        self.board_y = board_y

    def update(self, location: Location) -> Trajectory:
        future = []
        next = self.kf.predict(location.x, location.y)
        future.append(Location(next[0], next[1], location.time))
        return Trajectory(future)


class PolyPredictor:
    def __init__(self, degree) -> None:
        self.history = deque(maxlen=20)
        self.degree = degree

    def update(self, location: Location) -> Trajectory:
        self.history.append(location)
        result_x = np.polyfit(range(1, len(self.history) + 1),
                              [loc.x for loc in self.history],
                              self.degree)
        result_y = np.polyfit(range(1, len(self.history) + 1),
                              [loc.y for loc in self.history],
                              self.degree)
        time = np.linspace(0, len(self.history) + 1, 10)
        x = np.polyval(result_x, time)
        y = np.polyval(result_y, time)
        future = [Location(x[i], y[i], location.time) for i in range(len(x))]
        return Trajectory(future)


KNOWN_LOCATIONS = [Location(110, 120, 1),
                   Location(120, 125, 2)]

KNOWN_LOCATIONS_2 = [Location(110, 120, 1),
                     Location(120, 125, 2),
                     Location(130, 130, 3),
                     Location(140, 135, 4),
                     Location(150, 140, 5),
                     Location(160, 145, 6),
                     Location(170, 150, 7),
                     Location(180, 155, 8)]

KNOWN_LOCATIONS_3 = [Location(110, 120, 1),
                     Location(120, 125, 2),
                     Location(130, 130, 3),
                     Location(140, 132, 4),
                     Location(150, 134, 5),
                     Location(160, 135, 6),
                     Location(170, 130, 7),]


def naive():
    img = np.zeros((480, 480, 3), np.uint8)
    cv2.rectangle(img, (100, 100), (300, 300), (220, 0, 0), 3)
    predictor = NaivePredictor()
    predictor.history[0] = KNOWN_LOCATIONS[0]
    cv2.circle(img, (int(KNOWN_LOCATIONS[0].x), int(KNOWN_LOCATIONS[0].y)),
               4, (0, 220, 20), -1)
    prediction = predictor.update(KNOWN_LOCATIONS[1])
    cv2.circle(img, (int(KNOWN_LOCATIONS[-1].x), int(KNOWN_LOCATIONS[-1].y)),
               4, (0, 220, 20), -1)
    for location in prediction.locations:
        cv2.circle(img, (int(location.x), int(location.y)),
                   4, (0, 20, 220), -1)
    cv2.imshow("Prediction", img)
    cv2.waitKey(0)


def kalman():
    img = np.zeros((480, 480, 3), np.uint8)
    cv2.rectangle(img, (100, 100), (300, 300), (220, 0, 0), 3)
    predictor = KalmanPredictor()
    last_loc = None
    for location in KNOWN_LOCATIONS_2:
        cv2.circle(img, (int(location.x), int(location.y)),
                   4, (0, 220, 20), -1)
        last_loc = predictor.update(location).locations[-1]
        cv2.circle(img, (int(last_loc.x), int(last_loc.y)),
                   6, (0, 20, 220), 1)
    for _ in range(50):
        last_loc = predictor.update(last_loc).locations[-1]
        cv2.circle(img, (int(last_loc.x), int(last_loc.y)),
                   6, (0, 20, 220), 1)
    cv2.imshow("Prediction", img)
    cv2.waitKey(0)


def func(x, a, b, c):
    return a * x ** 2 + b * x + c


def poly():
    img = np.zeros((480, 480, 3), np.uint8)
    cv2.rectangle(img, (100, 100), (300, 300), (220, 0, 0), 3)
    predictor = PolyPredictor()
    last_loc = None
    for location in KNOWN_LOCATIONS_3:
        cv2.circle(img, (int(location.x), int(location.y)),
                   4, (0, 220, 20), -1)
        last_loc = predictor.update(location).locations[-1]
        cv2.circle(img, (int(last_loc.x), int(last_loc.y)),
                   6, (0, 20, 220), 1)
    for _ in range(50):
        last_loc = predictor.update(last_loc).locations[-1]
        cv2.circle(img, (int(last_loc.x), int(last_loc.y)),
                   6, (0, 20, 220), 1)
        cv2.imshow("Prediction", img)
        cv2.waitKey(0)


if __name__ == "__main__":
    naive()
    kalman()
    poly()
