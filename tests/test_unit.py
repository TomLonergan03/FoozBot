import unittest
from unittest.mock import MagicMock, patch
import cv2
import numpy as np
import PlayerController
import TrajectoryAdapter
from TrajectoryAdapter import Location, Trajectory
import BallDetectionAdapter
import ArduinoInterface

class PlayerControllerTestCase(unittest.TestCase):


    def setUp(self):
        self.mock_arduino = MagicMock()
        self.player_controller = PlayerController.PlayerController(
            ball_coords=(100, 200),
            first_row_x=100,
            first_row_y=120,
            second_row_x=200,
            second_row_y=220,
            start_coords=(0, 0),
            max_coords=(360, 240),
            arduino_interface=self.mock_arduino
        )

    def passes(self):
        self.assertTrue(True)

    def test_within_kicking_range(self):
        self.assertTrue(self.player_controller.within_kicking_range((100, 200), 124))
        self.assertFalse(self.player_controller.within_kicking_range((100, 200), 150))

    def test_first_row_kick(self):
        self.player_controller.first_row_kick(time.time())
        self.mock_arduino.kick.assert_called_once_with(1)

    def test_second_row_kick(self):
        self.player_controller.second_row_kick(time.time())
        self.mock_arduino.kick.assert_called_once_with(2)

    def test_players_horizontal_or_vertical(self):
        self.player_controller.players_horizontal_or_vertical((50, 50))
        self.mock_arduino.go_vertical.assert_called_with(1)
        self.mock_arduino.go_vertical.assert_called_with(2)

        self.player_controller.players_horizontal_or_vertical((150, 150))
        self.mock_arduino.go_horizontal.assert_called_with(1)
        self.mock_arduino.go_horizontal.assert_called_with(2)

    def test_move_players(self):
        self.mock_arduino.move_to.side_effect = lambda player, position: None

        self.player_controller.move_players([None, None])
        self.mock_arduino.move_to.assert_any_call(1, 55)
        self.mock_arduino.move_to.assert_any_call(2, 55)

        self.player_controller.move_players([120, 220])
        self.mock_arduino.move_to.assert_any_call(1, 110)
        self.mock_arduino.move_to.assert_any_call(2, 110)

    def test_check_kicking_cooldown(self):
        self.player_controller.first_row_kicking = True
        self.player_controller.second_row_kicking = True
        self.player_controller.last_kick_time = [time.time() - 1, time.time() - 1]

        self.player_controller.check_kicking_cooldown(time.time())
        self.assertFalse(self.player_controller.first_row_kicking)
        self.assertFalse(self.player_controller.second_row_kicking)

class TrajectoryAdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.trajectory_adapter = TrajectoryAdapter.TrajectoryAdapter(
            player_row_1=100,
            player_row_2=200,
            top_left=(0, 0),
            bottom_right=(360, 240)
        )

    def test_get_new_intersections(self):
        with patch.object(TrajectoryAdapter.Model, 'update') as mock_update:
            mock_update.return_value = [
                Location(0, 0, 0),
                Location(50, 50, 1),
                Location(100, 90, 2),
                Location(150, 150, 3),
                Location(200, 210, 4),
                Location(250, 220, 5)
            ]

            last_known_position = Location(0, 0, 0)
            intersections = self.trajectory_adapter.get_new_intersections(last_known_position)

            self.assertEqual(intersections, [90, 210])
            mock_update.assert_called_once_with(last_known_position)

    def test_draw_trajectory_on_frame(self):
        mock_frame = np.zeros((240, 360, 3), dtype=np.uint8)
        trajectory = Trajectory([
            Location(0, 0, 0),
            Location(50, 50, 1),
            Location(100, 100, 2),
            Location(150, 150, 3)
        ])

        self.trajectory_adapter.draw_trajectory_on_frame(mock_frame, trajectory)

        # Add assertions to check that the trajectory was drawn correctly on the frame

class BallDetectionAdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.ball_detection = BallDetectionAdapter.BallEdgeDetection(src=0)

    def test_get_ball_position(self):
        with patch.object(self.ball_detection.vs, 'read') as mock_read:
            mock_read.return_value = cv2.imread('test_image.jpg')

            ball_position = self.ball_detection.get_ball_position()

            # Add assertions to check that the ball position was detected correctly

    def test_get_top_left_bottom_right(self):
        with patch.object(self.ball_detection.vs, 'read') as mock_read:
            mock_read.return_value = cv2.imread('test_image.jpg')

            top_left, bottom_right = self.ball_detection.get_top_left_bottom_right()

            # Add assertions to check that the top-left and bottom-right coordinates were calculated correctly

    def test_get_players_x(self):
        with patch.object(self.ball_detection.vs, 'read') as mock_read:
            mock_read.return_value = cv2.imread('test_image.jpg')

            player_x, player_y = self.ball_detection.get_players_x()

            # Add assertions to check that the player row coordinates were detected correctly

class ArduinoInterfaceTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_serial = MagicMock()
        self.arduino_interface = ArduinoInterface.ArduinoInterface()
        self.arduino_interface.player2 = self.mock_serial

    def test_send_command(self):
        self.arduino_interface.send_command("test command")
        self.mock_serial.write.assert_called_once_with(b"test command")

    def test_go_vertical(self):
        self.arduino_interface.go_vertical(1)
        self.mock_serial.write.assert_not_called()

        self.arduino_interface.go_vertical(2)
        self.mock_serial.write.assert_called_with(b"player stand")

    def test_go_horizontal(self):
        self.arduino_interface.go_horizontal(1)
        self.mock_serial.write.assert_not_called()

        self.arduino_interface.go_horizontal(2)
        self.mock_serial.write.assert_called_with(b"player horizontal")

    def test_kick(self):
        self.arduino_interface.kick(1)
        self.mock_serial.write.assert_not_called()

        self.arduino_interface.kick(2)
        self.mock_serial.write.assert_called_with(b"player kick")

    def test_move_to(self):
        self.arduino_interface.move_to(1, 50)
        self.mock_serial.write.assert_not_called()

        self.arduino_interface.move_to(2, 75)
        self.mock_serial.write.assert_called_with(b"lateral 75")

if __name__ == '__main__':
    unittest.main()