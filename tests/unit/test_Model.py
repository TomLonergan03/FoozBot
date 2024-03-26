import unittest
from model import Model, Location
from TrajectoryAdapter import TrajectoryAdapter, Trajectory

class TestModel(unittest.TestCase):
    def test_model_initialization(self):
        initial_pos = Location(0, 0, 0)
        model = Model(initial_pos)
        self.assertEqual(model.history[0], initial_pos)
        self.assertEqual(model.friction, 1)
        self.assertEqual(model.x_attraction_force, 0)
        self.assertEqual(model.y_attraction_force, 0)
        self.assertEqual(model.board_min_x, 0)
        self.assertEqual(model.board_min_y, 0)
        self.assertEqual(model.board_max_x, 200)
        self.assertEqual(model.board_max_y, 200)
        self.assertEqual(model.iterations, 200)
        self.assertEqual(model.friction_limit, 0)
        self.assertEqual(model.attraction_min_speed, 0)

    def test_update_method(self):
        initial_pos = Location(0, 0, 0)
        model = Model(initial_pos)
        location = Location(10, 20, 1)
        trajectory = model.update(location)
        self.assertEqual(len(trajectory), 201)
        self.assertIsInstance(trajectory[0], Location)

    def test_calculate_future_location(self):
        initial_pos = Location(0, 0, 0)
        model = Model(initial_pos)
        trajectory = [Location(0, 0, 0), Location(10, 20, 1)]
        future_location = model.calculateFutureLocation(trajectory, 1)
        self.assertIsInstance(future_location, Location)
        self.assertAlmostEqual(future_location.x, 20, delta=0.1)
        self.assertAlmostEqual(future_location.y, 40, delta=0.1)


if __name__ == '__main__':
    unittest.main()