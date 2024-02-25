import BallDetectionAdapter
import TrajectoryAdapter
import PlayerController
import field_bounds_detect

trajectory_finder = TrajectoryAdapter.TrajectoryAdapter(5, 10)

# returns tuple (origin_x, origin_y, max_x, max_y)
table_bounds = field_bounds_detect.get_table_bounds()

ball_start_position = BallDetectionAdapter.get_ball_position()

FIRST_PLAYER_ROW = 5
SECOND_PLAYER_ROW = 10

player_controller = PlayerController.PlayerController(table_bounds, ball_start_position, FIRST_PLAYER_ROW, SECOND_PLAYER_ROW, table_bounds)

while True:
    ball_position = BallDetectionAdapter.get_ball_position()

    new_player_row_intersections = trajectory_finder.get_new_intersections(ball_position)

    # This handles player movement
    player_controller.update_ball_position(new_player_row_intersections)
