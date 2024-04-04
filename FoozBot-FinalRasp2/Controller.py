import threading
import time

import cv2
import numpy as np
from ArduinoInterface import ArduinoInterface
import BallDetectionAdapter
import PlayerController
import TrajectoryAdapter
from AppInterface import AppInterface
from GoalSensorInterface import GoalSensorInterface
from Mocks.MockArduinoInterface import MockArduinoInterface
from TrajectoryAdapter import Location
import serial

class Controller:

    def start(self):
        # MOTOR INTERFACE
        player_1_serial = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1,write_timeout=1)
        player_2_serial = serial.Serial('/dev/ttyACM1', baudrate=9600,timeout=1,write_timeout=1)      # /dev/ttyACM0 on Linux
        # player_1_serial = serial.Serial()
        arduino_interface = ArduinoInterface(player_1_serial,player_2_serial)
        time.sleep(2)
        arduino_interface.pon() 
        time.sleep(2)

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

        # GOAL SENSOR INTERFACE
        goal_sensor_interface = GoalSensorInterface()
        print("here detect")
        goal_detection_thread = threading.Thread(target=goal_sensor_interface.detect_score)
        goal_detection_thread.daemon = True
        goal_detection_thread.start()

        # APP INTERFACE
        app_interface = AppInterface("FoozbotMobileApp-master/score.json")

        start_time = time.time()    # Can be exchanged for the vision controlled frame number
        DISPLAY = True


        app_interface.wait_for_game_start()
        while app_interface.game_ongoing():
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
                cv2.namedWindow("System Visualisation", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("System Visualisation", 1080, 720)
                cv2.imshow("System Visualisation", image)


            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                app_interface.end_game()
                break

        print("Escapes loop")
        app_interface.end_game()
        print("Ends")
        ball_vision.vs.stop()
        cv2.destroyAllWindows()
        goal_sensor_interface.close_sensors()
        
        time.sleep(2)
        arduino_interface.poff()

        
        # Close the sensor connections when the program exits
        
