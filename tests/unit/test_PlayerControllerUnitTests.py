import time
import unittest
from unittest.mock import MagicMock

import PlayerController


class PlayerControllerTestCase(unittest.TestCase):


    def setUp(self):
        self.mock_arduino = MagicMock()
        self.player_controller = PlayerController.PlayerController(
            ball_coords=(0, 0),
            first_row_x=100,
            first_row_y=150,
            second_row_x=200,
            second_row_y=250,
            start_coords=(0, 0),
            max_coords=(360, 240),
            arduino_interface=self.mock_arduino
        )

    def test_passes(self):
        self.assertTrue(True)

    def test_within_kicking_range(self):
        self.assertTrue(self.player_controller.within_kicking_range((100, 200), 108))
        self.assertFalse(self.player_controller.within_kicking_range((100, 200), 150))

    def test_first_row_kick(self):
        self.player_controller.first_row_kick(time.time())
        self.mock_arduino.kick.assert_called_once_with(1)

    def test_second_row_kick(self):
        self.player_controller.second_row_kick(time.time())
        self.mock_arduino.kick.assert_called_once_with(2)
        
    # Need to fix this test
    # def test_players_horizontal_or_vertical(self):
    #     self.player_controller.players_horizontal_or_vertical((50, 50))
    #     self.mock_arduino.go_vertical.assert_called_with(2)

    #     self.player_controller.players_horizontal_or_vertical((150, 150))
    #     self.mock_arduino.go_horizontal.assert_called_with(1)
    #     self.mock_arduino.go_horizontal.assert_called_with(2)

    def test_move_players_no_intersection_points(self):
        intersect_pts = [None, None]
        ball_coords = (180, 120)
        self.player_controller.move_players(intersect_pts, ball_coords)
        self.mock_arduino.move_to.assert_called_with(2, 55.0)

    def test_move_players_row1_intersection(self):
        intersect_pts = [60, None]
        ball_coords = (180, 120)
        self.player_controller.move_players(intersect_pts, ball_coords)
        self.mock_arduino.move_to.assert_called_with(1, 75.0)

    def test_move_players_row2_intersection(self):
        intersect_pts = [None, 180]
        ball_coords = (180, 120)
        self.player_controller.move_players(intersect_pts, ball_coords)
        self.mock_arduino.move_to.assert_called_with(2, 75.0)

    def test_move_players_both_intersections(self):
        intersect_pts = [60, 180]
        ball_coords = (180, 120)
        self.player_controller.move_players(intersect_pts, ball_coords)
        self.mock_arduino.move_to.assert_any_call(1, 75.0)
        self.mock_arduino.move_to.assert_called_with(2, 75.0)
        
    # def test_check_kicking_cooldown(self):
    #     self.player_controller.first_row_kicking = True
    #     self.player_controller.second_row_kicking = True
    #     self.player_controller.last_kick_time = [time.time() - 1, time.time() - 1]

    #     self.player_controller.check_kicking_cooldown(time.time())
    #     self.assertFalse(self.player_controller.first_row_kicking)
    #     self.assertFalse(self.player_controller.second_row_kicking)
