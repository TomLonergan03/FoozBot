import unittest
from unittest.mock import MagicMock, patch
import cv2
import numpy as np
import PlayerController
import TrajectoryAdapter
from TrajectoryAdapter import Location, Trajectory
import BallDetectionAdapter
import ArduinoInterface
import time

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

    def test_players_horizontal_or_vertical(self):
        self.player_controller.players_horizontal_or_vertical((50, 50))
        self.mock_arduino.go_vertical.assert_called_with(2)
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
