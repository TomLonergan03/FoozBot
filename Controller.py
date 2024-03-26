import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
import serial

import ArduinoInterface
import BallDetectionAdapter
import PlayerController
import TrajectoryAdapter
from TrajectoryAdapter import Location

# MOTOR INTERFACE
player_1_serial = serial.Serial(player_1_port='/dev/ttyACM0', baudrate=9600, timeout=1,write_timeout=1)
player_2_serial = serial.Serial(player_2_port='COM5', baudrate=9600,timeout=1,write_timeout=1)
arduino_interface = ArduinoInterface.ArduinoInterface(player_1_serial,player_2_serial) # MockArduinoInterface.MockArduinoInterface()


# VISION
ball_vision = BallDetectionAdapter.BallEdgeDetection(src=0)
top_left, bottom_right = ball_vision.get_top_left_bottom_right()
temp = ball_vision.get_players_x()
players_pos = temp[0]
player_start = temp[1]
assert players_pos != [], "Players row signifiers not found. Please check camera source or replace the blue tape."
if players_pos[0] > players_pos[1]:
    FIRST_PLAYER_ROW = players_pos[0]
    SECOND_PLAYER_ROW = players_pos[1]
else:
    FIRST_PLAYER_ROW = players_pos[1]
    SECOND_PLAYER_ROW = players_pos[0]
# PATH PREDICTION
trajectory_finder = TrajectoryAdapter.TrajectoryAdapter(FIRST_PLAYER_ROW, SECOND_PLAYER_ROW, top_left= top_left, bottom_right= bottom_right)


# PLAYER CONTROLS
"""The table is measured from the top left (0,0), we need the bottom right (x,y) to define the playing field"""
player_controller = PlayerController.PlayerController(ball_vision.get_ball_position(), FIRST_PLAYER_ROW, player_start[0],
                                                      SECOND_PLAYER_ROW, player_start[1], top_left, bottom_right, arduino_interface)


start_time = time.time()    # Can be exchanged for the vision controlled frame number 
DISPLAY = True

# Initialize variables for logging and plotting
frame_times = []
frame_numbers = []
start_time = time.time()

predicted_trajectories = []
actual_trajectories = []
"""
# Create a figure and axis for the plot
fig, ax = plt.subplots()
ax.set_xlabel('Frame Number')
ax.set_ylabel('Frame Time (ms)')
ax.set_title('Real-time Performance Graph')

fig_trajectory, ax_trajectory = plt.subplots()
ax_trajectory.set_xlabel('X')
ax_trajectory.set_ylabel('Y')
ax_trajectory.set_title('Trajectory Prediction Accuracy')

def update_plot():
    ax.clear()
    ax.plot(frame_numbers, frame_times)
    ax.set_xlabel('Frame Number')
    ax.set_ylabel('Frame Time (ms)')
    ax.set_title('Real-time Performance Graph')
    fig.canvas.draw()
    
def update_trajectory_plot():
    ax_trajectory.clear()
    for predicted_path, actual_path in zip(predicted_trajectories, actual_trajectories):
        predicted_x = [loc.x for loc in predicted_path.locations]
        predicted_y = [loc.y for loc in predicted_path.locations]
        actual_x = [loc[0] for loc in actual_path]
        actual_y = [loc[1] for loc in actual_path]
        ax_trajectory.plot(predicted_x, predicted_y, 'b-', label='Predicted')
        ax_trajectory.plot(actual_x, actual_y, 'r--', label='Actual')
    ax_trajectory.set_xlabel('X')
    ax_trajectory.set_ylabel('Y')
    ax_trajectory.set_title('Trajectory Prediction Accuracy')
    ax_trajectory.legend()
    fig_trajectory.canvas.draw()

# Start the plot update timer
plot_timer = fig.canvas.new_timer(interval=1000)  # Update every 1 second
plot_timer.add_callback(update_plot)
plot_timer.start()

trajectory_plot_timer = fig_trajectory.canvas.new_timer(interval=5000)  # Update every 5 seconds
trajectory_plot_timer.add_callback(update_trajectory_plot)
trajectory_plot_timer.start()

plt.ion()  # Enable interactive mode
plt.show(block=False)  # Show the plot window
"""
while True:
    # Vision
    ball_position = ball_vision.get_ball_position()
    if ball_position is not None:

        # Trajectory Prediction
        ball_position_timestamp = Location(ball_position[0], ball_position[1], ball_vision.frame_no)    # can alternatively use frame number instead of time
        new_player_row_intersections = trajectory_finder.get_new_intersections(ball_position_timestamp)

        # PlayerControls
        player_controller.update_ball_position(ball_position, new_player_row_intersections, time.time())

    if DISPLAY:
        image = ball_vision.get_frame()
        trajectory_finder.draw_trajectory_on_frame(image, trajectory_finder.current_predicted_path)
        player_controller.draw_intersections_on_frame(image)
        # print("Ball position: " + str(ball_position) + "   " + str("Bottom right: " + str(bottom_right)))

        width, height = 400, 400  # Set the desired width and height of the image
        white_frame = np.ones((height, width, 3), dtype=np.uint8) * 255  # 3 channels for RGB, filled with white color

        player_controller.draw_text(image)
        cv2.imshow("System Visualisation", image)
        
    # Store predicted and actual trajectories
    predicted_trajectories.append(trajectory_finder.current_predicted_path)
    actual_trajectories.append(ball_vision.get_ball_position())
    # Log the frame time and frame number
    frame_time = time.time() - start_time
    frame_times.append(frame_time)
    frame_numbers.append(ball_vision.frame_no)

    # Pause to allow plot updates
    plt.pause(0.001)


    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
