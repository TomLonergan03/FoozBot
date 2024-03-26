import unittest
from unittest.mock import MagicMock
from PlayerController import PlayerController
from ArduinoInterface import ArduinoInterface

class TestPlayerController(unittest.TestCase):
    def setUp(self):
        self.arduino_interface = MagicMock(spec=ArduinoInterface)
        self.player_controller = PlayerController(
            ball_coords=(0, 0),
            first_row_x=100,
            first_row_y=50,
            second_row_x=200,
            second_row_y=100,
            start_coords=(0, 0),
            max_coords=(300, 150),
            arduino_interface=self.arduino_interface
        )

    def test_move_players_with_valid_intersect_points(self):
        intersect_pts = [50, 100]
        ball_coords = (150, 75)
        self.player_controller.move_players(intersect_pts, ball_coords)
        self.arduino_interface.move_to.assert_any_call(1, 50.0)
        self.arduino_interface.move_to.assert_any_call(2, 50.0)

    def test_move_players_with_intersect_points_out_of_range(self):
        intersect_pts = [200, 300]
        ball_coords = (250, 125)
        self.player_controller.move_players(intersect_pts, ball_coords)
        self.arduino_interface.move_to.assert_any_call(1, 110)
        self.arduino_interface.move_to.assert_any_call(2, 110)

    def test_move_players_with_intersect_points_below_range(self):
        intersect_pts = [-50, -100]
        ball_coords = (50, 25)
        self.player_controller.move_players(intersect_pts, ball_coords)
        self.arduino_interface.move_to.assert_any_call(1, 0)
        self.arduino_interface.move_to.assert_any_call(2, 0)

    def test_move_players_with_none_intersect_points(self):
        intersect_pts = [None, None]
        ball_coords = (150, 75)
        self.player_controller.move_players(intersect_pts, ball_coords)
        self.arduino_interface.move_to.assert_called_once_with(2, 50.0)

    def test_move_players_with_one_none_intersect_point(self):
        intersect_pts = [50, None]
        ball_coords = (150, 75)
        self.player_controller.move_players(intersect_pts, ball_coords)
        self.arduino_interface.move_to.assert_any_call(1, 50.0)
        self.arduino_interface.move_to.assert_any_call(2, 50.0)

if __name__ == '__main__':
    unittest.main()