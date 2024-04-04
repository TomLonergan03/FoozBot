import PCInterface
import ArduinoInterface
import cv2

class AdvancedPlayer(PCInterface):
    def __init__(self, ball_coords: tuple[float, float], first_row_x, first_row_y, second_row_x, second_row_y,
                 start_coords: tuple[float, float], max_coords: tuple[float, float], arduino_interface : ArduinoInterface):
        self.ball_coords = ball_coords

        # These fields store the positions of the rows of players on the board    
        self.player_row_x = [first_row_x, second_row_x]
        self.player_row_bottom = [first_row_y, second_row_y]        # For drawing purposes
        
        # Fields to tell us if the players are already in the process of kicking
        self.first_row_kicking = False
        self.second_row_kicking = False

        # Describes how far away the players can hit the ball
        self.KICKING_RANGE = 30
        self.PLAYER_WIDTH = 5

        # Describes how long it takes the players to kick
        self.kicking_cooldown = 1.25
        self.last_kick_time = [0, 0]

        # Command sending
        self.cmd_send_cooldown = 0.2
        self.last_cmd_sent = 0

        # Tells us which players are horizontal (so they don't get in the way of the ball from behind)
        self.first_row_horizontal = None
        self.second_row_horizontal = None

        # Maximum coordinates of the field
        self.start_coords = start_coords
        self.max_coords = max_coords
        self.coords_range = (
        max_coords[0] - start_coords[0], max_coords[1] - start_coords[1])  # effectively the w and h of the field

        self.arduino_interface = arduino_interface
        # assert isinstance(self.arduino_interface, ArduinoInterface)
        self.last_known_player_intersections = [0.0, 0.0]
        self.arduino_interface.send_command()

    def update_ball_position(self, ball_coords, player_intersections: list[float], time):
        self.ball_coords = ball_coords

        if player_intersections[0] is not None:
            self.last_known_player_intersections[0] = player_intersections[0]
        if player_intersections[1] is not None:
            self.last_known_player_intersections[1] = player_intersections[1]
        
        # Wind up kick?
        # Aim kick towards center of the field?


    # Returns which player should hit the ball; 0, 1 or 2
    def which_players_zone(self, x_intercept: float):
        # """
        if self.player_zone_coords(0)[0] < x_intercept < self.player_zone_coords(0)[1]:
            return 0
        if self.player_zone_coords(1)[0] < x_intercept < self.player_zone_coords(1)[1]:
            return 1
        if self.player_zone_coords(2)[0] < x_intercept < self.player_zone_coords(2)[1]:
            return 2

    def player_zone_coords(self, player_no):
        min_y = self.start_coords[1]
        h = self.coords_range[1]
        max_y = self.max_coords[1]

        if player_no == 0:
            return (int(min_y), int(min_y + h / 3))
        if player_no == 1:
            return (int(min_y + h / 3), int(min_y + (2 * h / 3)))
        if player_no == 2:
            return (int(min_y + (2 * h / 3)), int(min_y + h))

    def players_horizontal_or_vertical(self, ball_position):    # maybe tell it to move to the side a bit while going up so it doesn't push the ball further back?
        ball_x_pos = ball_position[0]

        if ball_x_pos > self.player_row_x[0]:
            if not self.first_row_horizontal or self.first_row_horizontal == None:
                self.arduino_interface.go_horizontal(1)
                # print("Row 1 go Horizontal")
                self.first_row_horizontal = True
        else:
            if self.first_row_horizontal or self.first_row_horizontal == None:
                self.arduino_interface.go_vertical(1)
                # print("Row 1 go Vertical")
                self.first_row_horizontal = False

        if ball_x_pos > self.player_row_x[1]:
            if not self.second_row_horizontal or self.second_row_horizontal == None:
                self.arduino_interface.go_horizontal(2)
                # print("Row 2 go Horizontal")
                self.second_row_horizontal = True
        else:
            if self.second_row_horizontal or self.second_row_horizontal == None:
                self.arduino_interface.go_vertical(2)
                # rint("Row 2 go Vertical")
                self.second_row_horizontal = False

    def first_row_kick(self, time):
        if not self.first_row_kicking:
            self.first_row_kicking = True
            self.last_kick_time[0] = time
            self.arduino_interface.kick(1)
            # print("Row 1 kick")

    def second_row_kick(self, time):
        if not self.second_row_kicking:
            self.second_row_kicking = True
            self.last_kick_time[1] = time
            self.arduino_interface.kick(2)
            print("Row 2 kick")

    def draw_intersections_on_frame(self, frame):
        pass

    def draw_text(self, frame):
        pass