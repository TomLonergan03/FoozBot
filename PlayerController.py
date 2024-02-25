import serial as serial
import time as time

import ArduinoInterface
import TrajectoryAdapter


class PlayerController:

    def __init__(self, bottom_right, ball_coords : tuple[float, float], first_row_x, second_row_x, max_coords : tuple[float, float]):
        self.ball_coords = ball_coords

        # These fields store the positions of the rows of players on the board
        #self.first_row_x = first_row_x
        #self.second_row_x = second_row_x
        self.player_row_x = [first_row_x, second_row_x]

        # Fields to tell us if the players are already in the process of kicking
        self.first_row_kicking = False
        self.second_row_kicking = False

        # Describes how far away the players can hit the ball
        self.kicking_range = 1
        self.kicking_width = 1

        # Describes how long it takes the players to kick
        self.kicking_cooldown = 1

        # Tells us which players are horizontal (so they don't get in the way of the ball from behind)
        self.first_row_horizontal = True
        self.second_row_horizontal = True

        # Maximum coordinates of the field
        self.max_coords = max_coords
        self.ta = TrajectoryAdapter.TrajectoryAdapter(first_row_x, second_row_x)


    def update_ball_position(self, ball_coords):
        self.ball_coords = ball_coords

        players_behind_ball = self.ball_behind_players()

        if players_behind_ball[0]:
            self.first_row_go_vertical()
        else:
            self.first_row_go_horizontal()

        if players_behind_ball[1]:
            self.second_row_go_vertical()
        else:
            self.second_row_go_horizontal()

        if self.within_kicking_range(ball_coords, self.first_row_y):
            self.first_row_kick()

        if self.within_kicking_range(ball_coords, self.second_row_y):
            self.second_row_kick()

    # Returns which player should hit the ball; 0, 1 or 2
    def which_players_zone(self, ball_coords):
        if 0 < ball_coords[1] < self.max_coords[1] / 3:
            return 0
        if self.max_coords[1] / 3 < ball_coords[1] < 2 * self.max_coords[1] / 3:
            return 1
        if 2 * self.max_coords[1] / 3 < ball_coords[1] < self.max_coords[1]:
            return 2

    def move_players(self, ball_coords):
        """ Pass current ball coordinates and decides how the player should move laterally."""
        # stepper motor moves from 0-110
        max_player_coord = self.max_coords[1] / 3

        intersect_pts = self.ta.get_new_intersections(ball_coords[0])

        if intersect_pts[0] is None:
            ArduinoInterface.ArduinoInterface.move_to(1, 55)
        else:
            player_in_row = self.which_players_zone(intersect_pts[0])
            assert player_in_row is not None, "ball wasn't within the maximum coordinates when deciding on closest player."
            lateral_percentage = (intersect_pts[0] - player_in_row * max_player_coord) / max_player_coord
            ArduinoInterface.ArduinoInterface.move_to(1, lateral_percentage * 110)
        
        if intersect_pts[1] is None:
            ArduinoInterface.ArduinoInterface.move_to(2, 55)
        else:
            player_in_row = self.which_players_zone(intersect_pts[1])
            assert player_in_row is not None, "ball wasn't within the maximum coordinates when deciding on closest player."
            lateral_percentage = (intersect_pts[1] - player_in_row * max_player_coord) / max_player_coord
            ArduinoInterface.ArduinoInterface.move_to(2, lateral_percentage * 110)

    """
        if player_in_row == 1:
            top_of_zone = self.width / 3
            bottom_of_zone = 0

            motor_move_position = 110 * ((top_of_zone - ball_coords[1]) / (self.width / 3))
            ArduinoInterface.ArduinoInterface.move_to(1, motor_move_position)
            ArduinoInterface.ArduinoInterface.move_to(2, motor_move_position)

        elif player_in_row == 2:
            top_of_zone = 2 * self.width / 3
            bottom_of_zone = self.width / 3
            motor_move_position = 110 * (
                        (top_of_zone - ball_coords[1]) / (top_of_zone - bottom_of_zone) + bottom_of_zone)
            ArduinoInterface.ArduinoInterface.move_to(1, motor_move_position)
            ArduinoInterface.ArduinoInterface.move_to(2, motor_move_position)
        elif player_in_row == 3:
            top_of_zone = self.width
            bottom_of_zone = 2 * self.width / 3
            motor_move_position = 110 * (
                        (top_of_zone - ball_coords[1]) / (top_of_zone - bottom_of_zone) + bottom_of_zone)
            ArduinoInterface.ArduinoInterface.move_to(1, motor_move_position)
            ArduinoInterface.ArduinoInterface.move_to(2, motor_move_position)
    """
        
    # Returns: (boolean, boolean) the bools represent if the ball is behind the first players and second players
    # respectively.
    def ball_behind_players(self):
        return_val = [False, False]
        if self.ball_coords[1] < self.first_row_y:
            return_val[0] = True

        if self.ball_coords[1] < self.second_row_y:
            return_val[1] = True

        return return_val

    def first_row_go_horizontal(self):
        if not self.first_row_horizontal:
            self.first_row_horizontal = True
            ArduinoInterface.ArduinoInterface.go_horizontal(1)

    def first_row_go_vertical(self):
        if self.first_row_horizontal:
            self.first_row_horizontal = False
            ArduinoInterface.ArduinoInterface.go_horizontal(1)

    def second_row_go_horizontal(self):
        if not self.second_row_horizontal:
            self.second_row_horizontal = True
            ArduinoInterface.ArduinoInterface.go_horizontal(2)

    def second_row_go_vertical(self):
        if self.second_row_horizontal:
            self.second_row_horizontal = False
            ArduinoInterface.ArduinoInterface(2)

    def first_row_kick(self):
        if not self.first_row_kicking:
            self.first_row_kicking = True
            ArduinoInterface.ArduinoInterface.kick(1)

    def second_row_kick(self):
        if not self.second_row_kicking:
            self.second_row_kicking = True
            ArduinoInterface.ArduinoInterface.kick(2)

    def within_kicking_range(self, ball_coords, players_y):
        if -1 < players_y - ball_coords[1] < 1:
            return True
        else:
            return False
