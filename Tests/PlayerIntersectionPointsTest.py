import unittest

from PlayerIntersectionPoints import PlayerIntersectionPoints


class MyTestCase(unittest.TestCase):

    #y = x, and players are at y = 2 and y = 8
    # should intersect at (2,2) and (8,8)
    def test_normal(self):
        pip = PlayerIntersectionPoints(2,8)

        intersection_points = pip.player_line_intersection_points(((1,0),1))

        self.assertEqual( ([2.,2.],[8.,8.]), intersection_points) # add assertion here

    #tests that the function returns [None,None], [None,None] if the line is horizontal and therefore there are no intersection points
    def test_horizontal(self):
        pip = PlayerIntersectionPoints(2,8)

        intersection_points = pip.player_line_intersection_points(((0,0),1))

        self.assertEqual([None,None], [None,None], intersection_points)

if __name__ == '__main__':
    unittest.main()
