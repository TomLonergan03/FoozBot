import BallDetectionAdapter
from Mocks import MockArduinoInterface
import PlayerController
import TrajectoryAdapter

trajectory_finder = TrajectoryAdapter.TrajectoryAdapter(5, 10)


# arduino_interface = ArduinoInterface.ArduinoInterface()
# This allows us to test the code when we don't have the arduino physically connected
arduino_interface = MockArduinoInterface.MockArduinoInterface()

# returns tuple (origin_x, origin_y, max_x, max_y)
ball_vision = BallDetectionAdapter.BallEdgeDetection()
bottom_right = ball_vision.get_bottom_right()


FIRST_PLAYER_ROW = 5
SECOND_PLAYER_ROW = 10

#The table is measured from the top left (0,0), we need the bottom right (x,y) to define the playing field
player_controller = PlayerController.PlayerController(ball_vision.get_ball_position(), FIRST_PLAYER_ROW, SECOND_PLAYER_ROW, bottom_right, arduino_interface)

while True:
    ball_position = ball_vision.get_ball_position(display=True)
    bottom_right = ball_vision.get_bottom_right(display=True)

    new_player_row_intersections = trajectory_finder.get_new_intersections(ball_position)

    # This handles player movement
    player_controller.update_ball_position(new_player_row_intersections)

    print("Ball position: " + str(ball_position) + "   " + str("Bottom right: " + str(bottom_right)))