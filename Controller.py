import cv2
import numpy as np

import BallDetectionAdapter
from Mocks import MockArduinoInterface
import PlayerController
import TrajectoryAdapter
from TrajectoryAdapter import Location
import time
from TrajectoryAdapter import Trajectory


def display_trajectory(image, trajectory: Trajectory, color=(0, 0, 255)):
    for i in range(1, len(trajectory.locations)):
        cv2.line(image, (int(trajectory.locations[i - 1].x), int(trajectory.locations[i - 1].y)),
                 (int(trajectory.locations[i].x), int(trajectory.locations[i].y)), color, 2)


trajectory_finder = TrajectoryAdapter.TrajectoryAdapter(5, 10)

KNOWN_LOCATIONS = [Location(110, 120, 1),
                   Location(120, 125, 2),
                   Location(130, 130, 3),
                   Location(140, 132, 4),
                   Location(150, 134, 5),
                   Location(160, 135, 6),
                   Location(170, 130, 7), ]

FRICTION = 0.01
ATTRACTION_FORCE = 0.00008
trajectory_model = TrajectoryAdapter.Model(KNOWN_LOCATIONS[0], friction=0.01, x_attraction_force=ATTRACTION_FORCE,
                                           y_attraction_force=ATTRACTION_FORCE)

start_time = time.time()

# arduino_interface = ArduinoInterface.ArduinoInterface()
# This allows us to test the code when we don't have the arduino physically connected
arduino_interface = MockArduinoInterface.MockArduinoInterface()

# returns tuple (origin_x, origin_y, max_x, max_y)
ball_vision = BallDetectionAdapter.BallEdgeDetection(src=4)
bottom_right = ball_vision.get_top_left_bottom_right()

FIRST_PLAYER_ROW = 5
SECOND_PLAYER_ROW = 10

# The table is measured from the top left (0,0), we need the bottom right (x,y) to define the playing field
player_controller = PlayerController.PlayerController(ball_vision.get_ball_position(), FIRST_PLAYER_ROW,
                                                      SECOND_PLAYER_ROW, bottom_right, arduino_interface)

future = []

while True:
    ball_position = ball_vision.get_ball_position()
    bottom_right = ball_vision.get_top_left_bottom_right()[1]

    #new_player_row_intersections = trajectory_finder.get_new_intersections(ball_position)
    # This handles player movement
    player_controller.update_ball_position

    frame = ball_vision.get_frame()
    if ball_position != None:
        image = np.zeros((480, 480, 3), np.uint8)
        ball_position_time = Location(ball_position[0], ball_position[1], time.time() - start_time)

        future = trajectory_model.update(ball_position_time)
        display_trajectory(frame, future)


    cv2.imshow("Frame", frame)

    print("Ball position: " + str(ball_position) + "   " + str("Bottom right: " + str(bottom_right)))
