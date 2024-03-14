from collections import deque
from dataclasses import dataclass
from typing import List
from model import Model
import cv2


@dataclass
class Location:
    x: float
    y: float
    frame_no: float


@dataclass
class Trajectory:
    locations: List[Location]


class TrajectoryAdapter:
    def __init__(self, player_row_1 : float, player_row_2 : float, top_left : tuple[float, float], bottom_right : tuple[float, float]):
        self.player_row_1 = player_row_1
        self.player_row_2 = player_row_2

        ATTRACTION_FORCE = 0.00008
        FRICTION = 0.01
        print(top_left[0])
        print(top_left[1])
        self.model = Model(initial_pos=Location(0, 0, 0), friction=FRICTION,
                           x_attraction_force=ATTRACTION_FORCE, y_attraction_force=ATTRACTION_FORCE,
                           board_min_x=top_left[0], board_min_y=top_left[1], board_max_x=bottom_right[0], board_max_y=bottom_right[1], iterations=200, friction_limit=FRICTION, attraction_min_speed=0.1)
        self.i = 1

        self.current_predicted_path = []

    def get_new_intersections(self, last_known_position):
        path = self.model.update(last_known_position)
        self.current_predicted_path = Trajectory(path)

        player_intersections = [None, None]
      #  print(path)
        for i in range(0, len(path) - 1):
            j = i + 1

            pos_1 = path[i]
            pos_2 = path[j]

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
        print(trajectory)
        assert type(trajectory) == Trajectory
        print(trajectory.locations[0])
       # print(trajectory)
        if len(trajectory.locations) == 0:
            return
        print(trajectory)
        print(len(trajectory.locations))
        for i in range(1, len(trajectory.locations)):
            cv2.line(image, (int(trajectory.locations[i - 1].x), int(trajectory.locations[i - 1].y)),
                     (int(trajectory.locations[i].x), int(trajectory.locations[i].y)), color, 2)

