import cv2


class PlayerController:

    def __init__(self, ball_coords: tuple[float, float], first_row_x, second_row_x, max_coords: tuple[float, float], arduino_interface):
        self.ball_coords = ball_coords

        # These fields store the positions of the rows of players on the board
        # self.first_row_x = first_row_x
        # self.second_row_x = second_row_x
        self.player_row_x = [first_row_x, second_row_x]

        # Fields to tell us if the players are already in the process of kicking
        self.first_row_kicking = False
        self.second_row_kicking = False

        # Describes how far away the players can hit the ball
        self.KICKING_RANGE = 1
        self.kicking_width = 1

        # Describes how long it takes the players to kick
        self.kicking_cooldown = 1

        # Tells us which players are horizontal (so they don't get in the way of the ball from behind)
        self.first_row_horizontal = True
        self.second_row_horizontal = True

        # Maximum coordinates of the field
        self.max_coords = max_coords
        
        self.arduino_interface = arduino_interface

        self.last_known_player_intersections = [0, 0]

    def update_ball_position(self, ball_coords, player_intersections):
        self.ball_coords = ball_coords

        if player_intersections[0] is not None:
            self.last_known_player_intersections[0] = player_intersections[0]
        if player_intersections[1] is not None:
            self.last_known_player_intersections[1] = player_intersections[1]

        self.players_horizontal_or_vertical(ball_coords)

        if self.within_kicking_range(ball_coords, self.player_row_x[0]):
            self.first_row_kick()

        if self.within_kicking_range(ball_coords, self.player_row_x[1]):
            self.second_row_kick()

        self.move_players(player_intersections)

    # Returns which player should hit the ball; 0, 1 or 2
    def which_players_zone(self, x_intercept : float):
        if 0 < x_intercept < (self.max_coords[1] / 3):
            return 0
        if self.max_coords[1] / 3 < x_intercept < 2 * self.max_coords[1] / 3:
            return 1
        if 2 * self.max_coords[1] / 3 < x_intercept < self.max_coords[1]:
            return 2

    def move_players(self, intersect_pts):
        """ Pass current ball coordinates and decides how the player should move laterally."""
        # stepper motor moves from 0-110
        max_player_coord = self.max_coords[1] / 3

        if intersect_pts[0] is None:
            self.arduino_interface.move_to(1, 55)
        else:
            player_in_row = self.which_players_zone(intersect_pts[0])
            if player_in_row is None:
                return
            lateral_percentage = (intersect_pts[0] - player_in_row * max_player_coord) / max_player_coord
            self.arduino_interface.move_to(1, lateral_percentage * 110)

        if intersect_pts[1] is None:
            self.arduino_interface.move_to(2, 55)
        else:
            player_in_row = self.which_players_zone(intersect_pts[1])
            if player_in_row is None:
                return
            lateral_percentage = (intersect_pts[1] - player_in_row * max_player_coord) / max_player_coord
            self.arduino_interface.move_to(2, lateral_percentage * 110)

    def should_kick(self, ball_coords):
        player_zone = self.which_players_zone(ball_coords)

        normalised_ball = ball_coords[1] - (player_zone * (self.max_coords[1] / 3))

        first_player = self.max_coords[1] * self.arduino_interface.get_position(1) / 110
        normalised_first_player = first_player - (player_zone * (self.max_coords[1] / 3))

        second_player = self.max_coords[1] * self.arduino_interface.get_position(2) / 110
        normalised_second_player = second_player - (player_zone * (self.max_coords[1] / 3))

        # if ball is in front of first players
        if ball_coords[0] > self.player_row_x[0]:
            if 0 <= (normalised_ball - normalised_first_player) < self.KICKING_RANGE:
                self.arduino_interface.kick(1)

        # if ball is in front of second players
        if ball_coords[0] > self.player_row_x[1]:
            if 0 <= (normalised_ball - normalised_second_player) < self.KICKING_RANGE:
                self.arduino_interface.kick(2)

    def players_horizontal_or_vertical(self, ball_position):
        ball_y_pos = ball_position[1]

        if ball_y_pos < self.player_row_x[0]:
            if not self.first_row_horizontal:
                self.arduino_interface.go_horizontal(1)
                self.first_row_horizontal = True
        elif self.first_row_horizontal:
            self.arduino_interface.go_vertical(1)
            self.first_row_horizontal = False

        if ball_y_pos < self.player_row_x[1]:
            if not self.second_row_horizontal:
                self.arduino_interface.go_horizontal(2)
                self.second_row_horizontal = True
        elif self.second_row_horizontal:
            self.arduino_interface.go_vertical(2)
            self.second_row_horizontal = False

    # Returns: (boolean, boolean) the bools represent if the ball is behind the first players and second players
    # respectively.
    def ball_behind_players(self):
        return_val = [False, False]
        if self.ball_coords[1] < self.player_row_x[0]:
            return_val[0] = True

        if self.ball_coords[1] < self.player_row_x[1]:
            return_val[1] = True

        return return_val

    def first_row_kick(self):
        if not self.first_row_kicking:
            self.first_row_kicking = True
            self.arduino_interface.kick(1)

    def second_row_kick(self):
        if not self.second_row_kicking:
            self.second_row_kicking = True
            self.arduino_interface.kick(2)

    def within_kicking_range(self, ball_coords, players_y):
        if self.KICKING_RANGE < players_y - ball_coords[1] < self.KICKING_RANGE:
            return True
        else:
            return False

    def draw_intersections_on_frame(self, frame):
        player_row_1 = self.player_row_x[0]
        player_row_2 = self.player_row_x[1]


        cv2.line(frame, (player_row_1,20), (player_row_1,200), color=(0,255,0), thickness=2)
        cv2.line(frame, (player_row_2,20), (player_row_2,200), color=(0,255,0), thickness=2)

        if self.last_known_player_intersections[0] is not None:
            cv2.circle(frame, (player_row_1, int(self.last_known_player_intersections[0])), radius=5, color=(255, 255, 0), thickness=5)

        if self.last_known_player_intersections[1] is not None:
            cv2.circle(frame, (player_row_2, int(self.last_known_player_intersections[1])), radius=5, color=(255, 255, 0), thickness=5)

        #cv2.circle(frame,(player_row_1, ))