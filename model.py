from collections import deque
from dataclasses import dataclass
from typing import List

import numpy as np
import cv2


@dataclass
class Location:
    x: float
    y: float
    time: float


@dataclass
class Trajectory:
    locations: List[Location]


def display_trajectory(image, trajectory: Trajectory, color=(0, 0, 255)):
    for i in range(1, len(trajectory.locations)):
        cv2.line(image, (int(trajectory.locations[i-1].x), int(trajectory.locations[i-1].y)),
                 (int(trajectory.locations[i].x), int(trajectory.locations[i].y)), color, 2)


KNOWN_LOCATIONS = [Location(110, 120, 1),
                   Location(120, 125, 2),
                   Location(130, 130, 3),
                   Location(140, 132, 4),
                   Location(150, 134, 5),
                   Location(160, 135, 6),
                   Location(170, 130, 7),]


class Model:
    def __init__(self, initial_pos: Location, friction: float = 1, x_attraction_force: float = 0, y_attraction_force: float = 0,  board_x: int = 200, board_y: int = 200):
        self.history = deque(maxlen=2)
        self.history.append(initial_pos)
        self.friction = 1 - friction
        self.x_attraction_force = x_attraction_force
        self.y_attraction_force = y_attraction_force
        self.board_x = board_x
        self.board_y = board_y

    def update(self, location: Location) -> Trajectory:
        self.history.append(location)
        future = []
        future.extend(self.history)
        for i in range(200):
            future.append(self.calculateFutureLocation(
                future, 0.1))
        return Trajectory([location] + future[2:])

    def calculateFutureLocation(self, trajectory: Trajectory, time: float) -> Location:
        dx = (trajectory[-1].x - trajectory[-2].x) / \
            (trajectory[-1].time - trajectory[-2].time)
        dy = (trajectory[-1].y - trajectory[-2].y) / \
            (trajectory[-1].time - trajectory[-2].time)

        # attract to the center
        dx -= (trajectory[-1].x - self.board_x) * self.x_attraction_force
        dy -= (trajectory[-1].y - self.board_y) * self.y_attraction_force

        # friction
        dx *= self.friction
        dy *= self.friction

        if trajectory[-1].x >= 300 or trajectory[-1].x <= 100:
            dx = -dx
        if trajectory[-1].y >= 300 or trajectory[-1].y <= 100:
            dy = -dy
        new_location = Location(
            trajectory[-1].x + dx * time, trajectory[-1].y + dy * time, trajectory[-1].time + time)
        return new_location


ATTRACTION_FORCE = 0.00008
FRICTION = 0.01

model = Model(KNOWN_LOCATIONS[0], FRICTION,
              ATTRACTION_FORCE, ATTRACTION_FORCE)
for i in range(1, len(KNOWN_LOCATIONS)):
    image = np.zeros((480, 480, 3), np.uint8)
    cv2.rectangle(image, (100, 100), (300, 300), (220, 0, 0), 3)
    display_trajectory(image, Trajectory(KNOWN_LOCATIONS[:i]), (0, 0, 255))
    future = model.update(KNOWN_LOCATIONS[i])
    display_trajectory(image, future, (0, 255, 0))
    cv2.imshow("trajectory", image)
    cv2.waitKey(0)