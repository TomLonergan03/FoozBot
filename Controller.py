import BallDetectionAdapter
# import TrajectoryAdapter
# import PlayerController
# import field_bounds_detect
import video
import cv2

# trajectory_finder = TrajectoryAdapter.TrajectoryAdapter(5, 10)

# # returns tuple (origin_x, origin_y, max_x, max_y)
# table_bounds = field_bounds_detect.get_table_bounds()

vision = BallDetectionAdapter.Vision(0)
ball_start_position = vision.update()

FIRST_PLAYER_ROW = 5
SECOND_PLAYER_ROW = 10

# player_controller = PlayerController.PlayerController(
#     table_bounds, ball_start_position, FIRST_PLAYER_ROW, SECOND_PLAYER_ROW, table_bounds)

try:
    while True:
        stuff, bottom_right = vision.update()
        location, frame_number, frame = stuff
        location = vision.unnormalise_coords(location[0], location[1])
        video.process_frame(frame, location, frame_number)
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
        # new_player_row_intersections = trajectory_finder.get_new_intersections(ball_position)

        # # This handles player movement
        # player_controller.update_ball_position(new_player_row_intersections)
finally:
    video.out.release()
