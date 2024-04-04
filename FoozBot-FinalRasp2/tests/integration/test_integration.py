import unittest
from unittest.mock import MagicMock, patch
import cv2
import Controller
import PlayerController
import TrajectoryAdapter
from TrajectoryAdapter import Location

class IntegrationTestCase(unittest.TestCase):
    @patch('Controller.BallDetectionAdapter.BallEdgeDetection')
    @patch('Controller.ArduinoInterface.ArduinoInterface')
    def setUp(self, mock_arduino, mock_ball_detection):
        self.mock_arduino = mock_arduino
        self.mock_ball_detection = mock_ball_detection

    def test_ball_behind_players(self, mock_arduino, mock_ball_detection):
        # Test when the ball is behind the first row of players
        mock_ball_detection.return_value.get_ball_position.return_value = (50, 50)
        mock_ball_detection.return_value.get_top_left_bottom_right.return_value = ((0, 0), (360, 240))
        mock_ball_detection.return_value.get_players_x.return_value = ([100], [120])
        mock_arduino.return_value.go_vertical.side_effect = lambda player: None

        Controller.run()

        mock_arduino.return_value.go_vertical.assert_called_with(1)
        self.assertFalse(mock_arduino.return_value.go_horizontal.called)

    def test_ball_in_front_of_players(self, mock_arduino, mock_ball_detection):
        # Test when the ball is in front of the second row of players
        mock_ball_detection.return_value.get_ball_position.return_value = (250, 200)
        mock_ball_detection.return_value.get_top_left_bottom_right.return_value = ((0, 0), (360, 240))
        mock_ball_detection.return_value.get_players_x.return_value = ([100], [120])
        mock_arduino.return_value.go_horizontal.side_effect = lambda player: None

        Controller.run()

        mock_arduino.return_value.go_horizontal.assert_called_with(1)
        mock_arduino.return_value.go_horizontal.assert_called_with(2)

    def test_kicking_range(self, mock_arduino, mock_ball_detection):
        # Test when the ball is within the kicking range of the first row of players
        mock_ball_detection.return_value.get_ball_position.return_value = (120, 180)
        mock_ball_detection.return_value.get_top_left_bottom_right.return_value = ((0, 0), (360, 240))
        mock_ball_detection.return_value.get_players_x.return_value = ([100], [120])
        mock_arduino.return_value.kick.side_effect = lambda player: None

        Controller.run()

        mock_arduino.return_value.kick.assert_called_with(1)

    def test_trajectory_prediction(self, mock_arduino, mock_ball_detection):
        # Test the trajectory prediction and player intersections
        mock_ball_detection.return_value.get_ball_position.return_value = (100, 200)
        mock_ball_detection.return_value.get_top_left_bottom_right.return_value = ((0, 0), (360, 240))
        mock_ball_detection.return_value.get_players_x.return_value = ([100], [120])
        mock_arduino.return_value.move_to.side_effect = lambda player, position: None

        with patch.object(TrajectoryAdapter.TrajectoryAdapter, 'get_new_intersections') as mock_get_intersections:
            mock_get_intersections.return_value = [150, 180]

            Controller.run()

            player_controller = Controller.player_controller
            mock_get_intersections.assert_called_with(Location(100, 200, Controller.ball_vision.frame_no))
            player_controller.update_ball_position.assert_called_with((100, 200), [150, 180], unittest.mock.ANY)

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()