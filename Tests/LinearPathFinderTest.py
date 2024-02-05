import unittest

from LinearPathFinder import LinearPathFinder


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    path_finder = LinearPathFinder()
    path_finder.update_coords([0,0])
    path_finder.update_coords([1,1])
    path_finder.update_coords([2,2])
    path_finder.update_coords([3,3])
    path_finder.update_coords([4,4])
    print(path_finder.compute_line())


    unittest.main()
