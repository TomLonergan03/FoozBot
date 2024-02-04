import numpy as np
from numpy.linalg import LinAlgError


class PlayerIntersectionPoints:

    def __init__(self, first_player_yline, second_player_yline):
        self.first_player_yline = first_player_yline
        self.second_player_yline = second_player_yline

    def player_line_intersection_points(self, equation_and_direction):
        # Ball trajectory equation
        m_ball = equation_and_direction[0][0]
        c_ball = equation_and_direction[0][1]

        # First player line
        m_first_players = 0
        c_first_players = self.first_player_yline

        # Second player line
        m_second_players = 0
        c_second_players = self.second_player_yline

        # First player line intersection point
        # Equation needs to be rearranged to ax + by = c
        a = np.array([[-m_ball,1],[-m_first_players,1]])
        b = np.array([c_ball,c_first_players])

        try:
            first_intersection = (np.linalg.solve(a,b)).tolist()
        except LinAlgError:
            first_intersection = (None, None)

        # Second player line intersection point
        a = np.array([[-m_ball,1],[-m_second_players,1]])
        b = np.array([c_ball,c_second_players])

        try:
            second_intersection = (np.linalg.solve(a,b)).tolist()
        except LinAlgError:
            second_intersection = (None,None)

        return (first_intersection,second_intersection)