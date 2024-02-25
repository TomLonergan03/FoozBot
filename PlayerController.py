import serial as serial
import time as time

import ArduinoInterface


class PlayerController:

    def __init__(self, bottom_right, ball_coords, first_row_y, second_row_y):
        self.ball_coords = ball_coords

        # These fields store the positions of the rows of players on the board
        self.first_row_y = first_row_y
        self.second_row_y = second_row_y

        # Fields to tell us if the players are already in the process of kicking
        self.first_row_kicking = False
        self.second_row_kicking = False

        # Describes how far away the players can hit the ball
        self.kicking_range = 1

        # Describes how long it takes the players to kick
        self.kicking_cooldown = 1

        # Tells us which players are horizontal (so they don't get in the way of the ball from behind)
        self.first_row_horizontal = True
        self.second_row_horizontal = True

        # Board width
        self.width = width

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

    # Returns which player should hit the ball; 1, 2 or 3
    def which_players_zone(self, ball_coords):
        if 0 < ball_coords < self.width / 3:
            return 1
        if self.width / 3 < ball_coords < 2 * self.width / 3:
            return 2
        if 2 * self.width / 3 < ball_coords < self.width:
            return 3

    def move_players(self, ball_coords):
        player_in_row = self.which_players_zone(ball_coords)

        # stepper motor moves from 0-110
        # for each third we calculate the relative y position of the ball in that third (from 0 to 1)
        # we then multiply this by the stepper
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
            ArduinoInterface.kick(2)

    def within_kicking_range(self, ball_coords, players_y):
        if -1 < players_y - ball_coords[1] < 1:
            return True
        else:
            return False
