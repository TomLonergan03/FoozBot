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

class TestTrajectoryAdapter(unittest.TestCase):
    def test_trajectory_adapter_initialization(self):
        adapter = TrajectoryAdapter(player_row_1=100, player_row_2=200, top_left=(0, 0), bottom_right=(300, 300))
        self.assertEqual(adapter.player_row_1, 100)
        self.assertEqual(adapter.player_row_2, 200)
        self.assertIsInstance(adapter.model, Model)

    def test_get_new_intersections(self):
        adapter = TrajectoryAdapter(player_row_1=100, player_row_2=200, top_left=(0, 0), bottom_right=(300, 300))
        last_known_position = Location(50, 50, 0)
        intersections = adapter.get_new_intersections(last_known_position)
        self.assertIsInstance(intersections, list)
        self.assertEqual(len(intersections), 2)

    def test_draw_trajectory_on_frame(self):
        adapter = TrajectoryAdapter(player_row_1=100, player_row_2=200, top_left=(0, 0), bottom_right=(300, 300))
        image = cv2.imread("test_image.jpg")
        trajectory = Trajectory([Location(0, 0, 0), Location(100, 100, 1), Location(200, 200, 2)])
        adapter.draw_trajectory_on_frame(image, trajectory)
        # Perform assertions to check if the trajectory is drawn correctly on the image

if __name__ == '__main__':
    unittest.main()