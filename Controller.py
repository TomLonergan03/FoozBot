import time
import cv2
import BallDetectionAdapter
import PlayerController
import TrajectoryAdapter
from Mocks import MockArduinoInterface
from TrajectoryAdapter import Location

# MOTOR INTERFACE
"""
arduino_interface = ArduinoInterface.ArduinoInterface()
This allows us to test the code when we don't have the arduino physically connected"""
arduino_interface = MockArduinoInterface.MockArduinoInterface()

# VISION
ball_vision = BallDetectionAdapter.BallEdgeDetection(src=0)
top_left, bottom_right = ball_vision.get_top_left_bottom_right()
temp = ball_vision.get_players_x()
players_pos = temp[0]
player_start = temp[1]
assert players_pos != [], "Players row signifiers not found. Please check camera source or replace the blue tape."
FIRST_PLAYER_ROW = players_pos[0]
SECOND_PLAYER_ROW = players_pos[1]

# PATH PREDICTION
trajectory_finder = TrajectoryAdapter.TrajectoryAdapter(FIRST_PLAYER_ROW, SECOND_PLAYER_ROW, top_left= top_left, bottom_right= bottom_right)


# PLAYER CONTROLS
"""The table is measured from the top left (0,0), we need the bottom right (x,y) to define the playing field"""
player_controller = PlayerController.PlayerController(ball_vision.get_ball_position(), FIRST_PLAYER_ROW, player_start[0],
                                                      SECOND_PLAYER_ROW, player_start[1], top_left, bottom_right, arduino_interface)


start_time = time.time()    # Can be exchanged for the vision controlled frame number 
DISPLAY = True

while True:
    # Vision
    ball_position = ball_vision.get_ball_position()
    if ball_position is not None:

        # Trajectory Prediction
        ball_position_timestamp = Location(ball_position[0], ball_position[1], time.time() - start_time)    # can alternatively use frame number instead of time
        new_player_row_intersections = trajectory_finder.get_new_intersections(ball_position_timestamp)

        # PlayerControls
        player_controller.update_ball_position(ball_position, new_player_row_intersections, time.time())

    if DISPLAY:
        image = ball_vision.get_frame()
        trajectory_finder.draw_trajectory_on_frame(image, trajectory_finder.current_predicted_path)
        player_controller.draw_intersections_on_frame(image)
        cv2.imshow("System Visualisation", image)
        # print("Ball position: " + str(ball_position) + "   " + str("Bottom right: " + str(bottom_right)))
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
