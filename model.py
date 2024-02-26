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
    def __init__(self, initial_pos: Location, friction: float = 1, x_attraction_force: float = 0, y_attraction_force: float = 0, board_min_x: int = 0, board_min_y: int = 0, board_max_x: int = 200, board_max_y: int = 200, iterations: int = 200, friction_limit: int = 0, attraction_min_speed: int = 0):
        self.history = deque(maxlen=2)
        self.history.append(initial_pos)
        self.friction = 1 - friction
        self.x_attraction_force = x_attraction_force
        self.y_attraction_force = y_attraction_force
        self.board_max_x = board_max_x
        self.board_max_y = board_max_y
        self.board_min_x = board_min_x
        self.board_min_y = board_min_y
        self.prediction = initial_pos
        self.iterations = iterations
        self.friction_limit = friction_limit
        self.attraction_min_speed = attraction_min_speed

    def update(self, location: Location) -> Trajectory:
        self.history.append(
            Location((location.x + self.prediction.x)/2, (location.y + self.prediction.y)/2, location.time))
        # self.history.append(location)
        future = []
        future.extend(self.history)
        for _ in range(self.iterations):
            future.append(self.calculateFutureLocation(
                future, 1))
        self.prediction = future[2]
        return Trajectory([location] + future[2:])

    def calculateFutureLocation(self, trajectory: Trajectory, time: float) -> Location:
        dx = (trajectory[-1].x - trajectory[-2].x) / \
            (trajectory[-1].time - trajectory[-2].time)
        dy = (trajectory[-1].y - trajectory[-2].y) / \
            (trajectory[-1].time - trajectory[-2].time)

        if abs(dx) > self.attraction_min_speed:
            dx -= (trajectory[-1].x - (self.board_max_x -
                                       self.board_min_x) / 2) ** 2 * self.x_attraction_force
        if abs(dy) > self.attraction_min_speed:
            dy -= (trajectory[-1].y - (self.board_max_y -
                                       self.board_min_y) / 2) * self.y_attraction_force

        # friction
        if abs(dx) > self.friction_limit:
            dx *= self.friction
        if abs(dy) > self.friction_limit:
            dy *= self.friction

        if trajectory[-1].x >= self.board_max_x or trajectory[-1].x <= self.board_min_x:
            dx = -dx
        if trajectory[-1].y >= self.board_max_y or trajectory[-1].y <= self.board_min_y:
            dy = -dy
        new_location = Location(
            trajectory[-1].x + dx * time, trajectory[-1].y + dy * time, trajectory[-1].time + time)
        return new_location


if __name__ == "__main__":
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
