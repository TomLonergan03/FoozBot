from collections import deque
from dataclasses import dataclass
from typing import List

import cv2


@dataclass
class Location:
    x: float
    y: float
    time: float


@dataclass
class Trajectory:
    locations: List[Location]




class Model:
    def __init__(self, initial_pos: Location, friction: float = 1, x_attraction_force: float = 0,
                 y_attraction_force: float = 0, board_min_x: int = 0, board_min_y: int = 0, board_max_x: int = 321,
                 board_max_y: int = 200):
        self.history = deque(maxlen=10)
        self.history.append(initial_pos)
        self.friction = 1 - friction
        self.x_attraction_force = x_attraction_force
        self.y_attraction_force = y_attraction_force
        self.board_max_x = board_max_x
        self.board_max_y = board_max_y
        self.board_min_x = board_min_x
        self.board_min_y = board_min_y

        self.current_prediction : Trajectory = Trajectory(Location(0, 0, 0))

    def update(self, location: Location) -> Trajectory:
        self.history.append(location)
        future = []
        future.extend(self.history)
        for i in range(10):
            future_location = self.calculateFutureLocation(
                future, 0.1)
            if future_location is not None:
                future.append(future_location)
        return Trajectory([location] + future[2:])

    def calculateFutureLocation(self, trajectory: Trajectory, time: float) -> Location:
        if trajectory[-1] is None or trajectory[-2] is None:
            return None

        if (trajectory[-1].time - trajectory[-2].time) == 0:
            trajectory[-1].time += 0.0000001

        dx = (trajectory[-1].x - trajectory[-2].x) / \
             (trajectory[-1].time - trajectory[-2].time)

        if (trajectory[-1].time - trajectory[-2].time):
            trajectory[-1].time += 0.0000001
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
    def __init__(self, player_row_1 : float, player_row_2 : float, top_left : tuple[float, float], bottom_right : tuple[float, float]):
        self.player_row_1 = player_row_1
        self.player_row_2 = player_row_2

        ATTRACTION_FORCE = 0.00008
        FRICTION = 0.01
        self.model = Model(Location(0, 0, 0), FRICTION,
                           ATTRACTION_FORCE, ATTRACTION_FORCE, 
                           top_left[0], top_left[1], bottom_right[0], bottom_right[1])
        self.i = 1

        self.current_predicted_path = Trajectory([Location(0,0,0)])

    def get_new_intersections(self, last_known_position):
        path = self.model.update(last_known_position)
        self.current_predicted_path = path

        player_intersections = [None, None]
        for i in range(0, len(path.locations) - 1):
            j = i + 1

            pos_1 = path.locations[i]
            pos_2 = path.locations[j]

            if (pos_1.x <= self.player_row_1 <= pos_2.x) or (pos_1.x >= self.player_row_1 >= pos_2.x):
                if player_intersections[0] is None: # Only catch the first intersection with each row of players
                    player_intersections[0] = pos_1.y 
                # Find which direction the ball is going in?

            if (pos_1.x <= self.player_row_2 <= pos_2.x) or (pos_1.x >= self.player_row_2 >= pos_2.x):
                if player_intersections[1] is None:
                    player_intersections[1] = pos_1.y
        # print(player_intersections)
        return player_intersections

    def draw_trajectory_on_frame(self,image, trajectory: Trajectory, color=(0, 0, 255)):
        if len(trajectory.locations) == 0:
            return

        for i in range(1, len(trajectory.locations)):
            cv2.line(image, (int(trajectory.locations[i - 1].x), int(trajectory.locations[i - 1].y)),
                     (int(trajectory.locations[i].x), int(trajectory.locations[i].y)), color, 2)

