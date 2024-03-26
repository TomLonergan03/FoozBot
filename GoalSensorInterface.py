
class GoalSensorInterface:
    def __init__(self):
        self.player_1_score = 0
        self.player_2_score = 0

    def player_score(self, player_no):
        if player_no == 1:
            self.player_1_score += 1
        if player_no ==2:
            self.player_2_score += 1
