import cv2

class PlayerController:

    def __init__(self, ball_coords: tuple[float, float], first_row_x, first_row_y, second_row_x, second_row_y, start_coords :tuple[float, float], max_coords: tuple[float, float], arduino_interface):
        self.ball_coords = ball_coords

        # These fields store the positions of the rows of players on the board
        # self.first_row_x = first_row_x
        # self.second_row_x = second_row_x
        self.player_row_x = [first_row_x, second_row_x]
        self.player_row_bottom = [first_row_y, second_row_y]

        # Fields to tell us if the players are already in the process of kicking
        self.first_row_kicking = False
        self.second_row_kicking = False

        # Describes how far away the players can hit the ball
        self.KICKING_RANGE = 24
        self.kicking_width = 8

        # Describes how long it takes the players to kick
        self.kicking_cooldown = 0.5
        self.last_kick_time = [0, 0]

        # Tells us which players are horizontal (so they don't get in the way of the ball from behind)
        self.first_row_horizontal = True
        self.second_row_horizontal = True

        # Maximum coordinates of the field
        self.start_coords = start_coords
        self.max_coords = max_coords
        self.coords_range = (max_coords[0] - start_coords[0], max_coords[1] - start_coords[1]) # effectively the w and h of the field
        
        self.arduino_interface = arduino_interface

        self.last_known_player_intersections = [0.0, 0.0]

    def update_ball_position(self, ball_coords, player_intersections : list[float], time):
        self.ball_coords = ball_coords

        if player_intersections[0] is not None:
            self.last_known_player_intersections[0] = player_intersections[0]
        if player_intersections[1] is not None:
            self.last_known_player_intersections[1] = player_intersections[1]

        self.players_horizontal_or_vertical(ball_coords)
        # self.should_kick(ball_coords)
        # """
        if self.within_kicking_range(ball_coords, self.player_row_x[0]):
            self.first_row_kick(time)

        if self.within_kicking_range(ball_coords, self.player_row_x[1]):
            self.second_row_kick(time)
        # """
        self.move_players(player_intersections)
        self.check_kicking_cooldown(time)

    # Returns which player should hit the ball; 0, 1 or 2
    def which_players_zone(self, x_intercept : float):
        min_y = self.start_coords[1]
        h = self.coords_range[1]
        max_y = self.max_coords[1]
        # """
        if min_y < x_intercept < min_y + h / 3:
            return 0
        if min_y + h / 3 < x_intercept < min_y + (2 * h / 3):
            return 1
        if min_y + (2 * h / 3) < x_intercept < max_y:
            return 2
        # """
        # return 0

    def move_players(self, intersect_pts):
        """ Pass current ball coordinates and decides how the player should move laterally."""
        # stepper motor moves from 0-110
        max_player_coord = self.coords_range[1] / 3

        if intersect_pts[0] is None:
            self.arduino_interface.move_to(1, 55)
        else:
            player_in_row = self.which_players_zone(intersect_pts[0])
            if player_in_row is not None:
                lateral_percentage = (intersect_pts[0] - player_in_row * max_player_coord - self.start_coords[1]) / max_player_coord
                self.arduino_interface.move_to(1, lateral_percentage * 110)
                print("Move row 1 to " + str(lateral_percentage * 110))

        if intersect_pts[1] is None:
            self.arduino_interface.move_to(2, 55)
        else:
            player_in_row = self.which_players_zone(intersect_pts[1])
            if player_in_row is not None:
                lateral_percentage = (intersect_pts[1] - player_in_row * max_player_coord - self.start_coords[1]) / max_player_coord
                self.arduino_interface.move_to(2, lateral_percentage * 110)
                print("Move row 2 to " + str(lateral_percentage * 110))
    """
    def should_kick(self, ball_coords):
        player_zone = self.which_players_zone(ball_coords[1])
        if player_zone is not None:
            normalised_ball = ball_coords[1] - (player_zone * (self.coords_range[1] / 3))

            first_player = self.start_coords[1] + self.coords_range[1] * self.arduino_interface.get_position(1) / 110
            normalised_first_player = first_player - (player_zone * (self.max_coords[1] / 3))

            second_player = self.start_coords[1] + self.coords_range[1] * self.arduino_interface.get_position(2) / 110
            normalised_second_player = second_player - (player_zone * (self.max_coords[1] / 3))

            # if ball is in front of first players
            if ball_coords[0] > self.player_row_x[0]:
                if 0 <= (normalised_ball - normalised_first_player) < self.KICKING_RANGE:
                    self.arduino_interface.kick(1)
                    print("Row 1 kick")

            # if ball is in front of second players
            if ball_coords[0] > self.player_row_x[1]:
                if 0 <= (normalised_ball - normalised_second_player) < self.KICKING_RANGE:
                    self.arduino_interface.kick(2)
                    print("Row 2 kick")
    """

    def players_horizontal_or_vertical(self, ball_position):
        ball_x_pos = ball_position[0]

        if ball_x_pos > self.player_row_x[0]:
            if not self.first_row_horizontal:
                self.arduino_interface.go_horizontal(1)
                print("Row 1 go Horizontal")
                self.first_row_horizontal = True
        elif self.first_row_horizontal and ball_x_pos <= self.player_row_x[0]:
            self.arduino_interface.go_vertical(1)
            print("Row 1 go Vertical")
            self.first_row_horizontal = False

        if ball_x_pos > self.player_row_x[1]:
            if not self.second_row_horizontal:
                self.arduino_interface.go_horizontal(2)
                print("Row 2 go Horizontal")
                self.second_row_horizontal = True
        elif self.second_row_horizontal and ball_x_pos <= self.player_row_x[1]:
            self.arduino_interface.go_vertical(2)
            print("Row 2 go Vertical")
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

    def first_row_kick(self, time):
        if not self.first_row_kicking:
            self.first_row_kicking = True
            self.last_kick_time[0] = time
            self.arduino_interface.kick(1)
            print("Row 1 kick")

    def second_row_kick(self, time):
        if not self.second_row_kicking:
            self.second_row_kicking = True
            self.last_kick_time[1] = time
            self.arduino_interface.kick(2)
            print("Row 2 kick")

    def within_kicking_range(self, ball_coords, players_x):
        if - self.KICKING_RANGE < (players_x - ball_coords[0]) < self.KICKING_RANGE:
            return True
        else:
            return False

    def check_kicking_cooldown(self, time):
        if time - self.last_kick_time[0] > self.kicking_cooldown:
            self.first_row_kicking = False
        if time - self.last_kick_time[1] > self.kicking_cooldown:
            self.second_row_kicking = False

    def draw_intersections_on_frame(self, frame):
        player_row_1 = int(self.player_row_x[0])
        player_row_2 = int(self.player_row_x[1])
        players_y_1 = int(self.player_row_bottom[0])
        players_y_2 = int(self.player_row_bottom[1])

        cv2.line(frame, (player_row_1, self.start_coords[1]), (player_row_1, players_y_1), color=(0,255,0), thickness=2)
        cv2.line(frame, (player_row_2, self.start_coords[1]), (player_row_2, players_y_2), color=(0,255,0), thickness=2)

        if self.last_known_player_intersections[0] is not None:
            cv2.circle(frame, (player_row_1, int(self.last_known_player_intersections[0])), radius=5, color=(255, 255, 0), thickness=5)

        if self.last_known_player_intersections[1] is not None:
            cv2.circle(frame, (player_row_2, int(self.last_known_player_intersections[1])), radius=5, color=(255, 255, 0), thickness=5)

        #cv2.circle(frame,(player_row_1, ))