
class PlayerController:
    def __init__(self, width, first_players_y, second_players_y):
        self.first_players_y = first_players_y
        self.second_players_y = second_players_y

        self.

        player_1_range = (0,width/3)
        player_2_range = (width/3,2*width/3)
        player_3_range = (2*width/3, width)

    def update_ball_position(self, ball_coords):
        self.ball_coords = ball_coords

    def ball_behind_players(self):
        if self.ball_coords[1] < self.first_players_y:
            self.goHorozontal(1)
        else:
            self.goVertical(1)

        if self.ball_coords[1] < self.second_players_y:
            self.goHorozontal(2)
        else:
            self.goVertical(2)


    def goHorozontal(self, players):
        # if

    def goVertical(self,players):