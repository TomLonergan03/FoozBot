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
        cv2.line(image, (int(trajectory.locations[i - 1].x), int(trajectory.locations[i - 1].y)),
                 (int(trajectory.locations[i].x), int(trajectory.locations[i].y)), color, 2)


KNOWN_LOCATIONS = [Location(110, 120, 1),
                   Location(120, 125, 2),
                   Location(130, 130, 3),
                   Location(140, 132, 4),
                   Location(150, 134, 5),
                   Location(160, 135, 6),
                   Location(170, 130, 7), ]


class Model:
    def __init__(self, initial_pos: Location, friction: float = 1, x_attraction_force: float = 0,
                 y_attraction_force: float = 0, board_min_x: int = 0, board_min_y: int = 0, board_max_x: int = 200,
                 board_max_y: int = 200):
        self.history = deque(maxlen=2)
        self.history.append(initial_pos)
        self.friction = 1 - friction
        self.x_attraction_force = x_attraction_force
        self.y_attraction_force = y_attraction_force
        self.board_max_x = board_max_x
        self.board_max_y = board_max_y
        self.board_min_x = board_min_x
        self.board_min_y = board_min_y

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
        dx -= (trajectory[-1].x - (self.board_max_x -
                                   self.board_min_x) / 2) * self.x_attraction_force
        dy -= (trajectory[-1].y - (self.board_max_y -
                                   self.board_min_y) / 2) * self.y_attraction_force

        # friction
        dx *= self.friction
        dy *= self.friction

        if trajectory[-1].x >= self.board_max_x or trajectory[-1].x <= self.board_min_x:
            dx = -dx
        if trajectory[-1].y >= self.board_max_y or trajectory[-1].y <= self.board_min_y:
            dy = -dy
        new_location = Location(
            trajectory[-1].x + dx * time, trajectory[-1].y + dy * time, trajectory[-1].time + time)
        return new_location


class TrajectoryAdapter:
    def __init__(self, player_row_1, player_row_2):
        self.player_row_1 = player_row_1
        self.player_row_2 = player_row_2

        ATTRACTION_FORCE = 0.00008
        FRICTION = 0.01
        self.model = Model(KNOWN_LOCATIONS[0], FRICTION,
                           ATTRACTION_FORCE, ATTRACTION_FORCE)
        self.i = 1

    def update_prediction(self, last_known_position):
        return self.model.update(KNOWN_LOCATIONS[self.i])

    def get_new_intersections(self, last_known_position):
        path = self.model.update(last_known_position)

        player_intersections = [None, None]
        for i in range(0, len(path.locations) - 1):
            j = i + 1

            pos_1 = path.locations[i]
            pos_2 = path.locations[j]

            if (pos_1.y <= self.player_row_1 <= pos_2.y) or (pos_1.y >= self.player_row_1 >= pos_2.y):
                player_intersections[0] = pos_1.x

            if (pos_1.y <= self.player_row_2 <= pos_2.y) or (pos_1.y >= self.player_row_2 >= pos_2.y):
                player_intersections[1] = pos_1.x
        return player_intersections

if __name__ == '__main__':
    ta = TrajectoryAdapter(50, 80)

    KNOWN_LOCATIONS = [Location(60, 60, 1),
                       Location(70, 70, 2),

        Location(110, 120, 1),
                       Location(120, 125, 2),
                       Location(130, 130, 3),
                       Location(140, 132, 4),
                       Location(150, 134, 5),
                       Location(160, 135, 6),
                       Location(170, 130, 7),]

    for i in range(1, len(KNOWN_LOCATIONS)):
        print(ta.get_new_intersections(KNOWN_LOCATIONS[i]))


