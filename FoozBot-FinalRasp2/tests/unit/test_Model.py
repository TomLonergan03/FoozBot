import unittest
from model import Model, Location
import random

class TestModel(unittest.TestCase):
    def setUp(self):
        self.initial_pos = Location(100, 100, 0)
        self.model = Model(self.initial_pos)

    def test_initialization(self):
        self.assertEqual(self.model.history[0], self.initial_pos)
        self.assertEqual(self.model.friction, 0)  # Update the expected value to 0
        self.assertEqual(self.model.x_attraction_force, 0)
        self.assertEqual(self.model.y_attraction_force, 0)
        self.assertEqual(self.model.board_min_x, 0)
        self.assertEqual(self.model.board_min_y, 0)
        self.assertEqual(self.model.board_max_x, 200)
        self.assertEqual(self.model.board_max_y, 200)
        self.assertEqual(self.model.iterations, 200)
        self.assertEqual(self.model.friction_limit, 0)
        self.assertEqual(self.model.attraction_min_speed, 0)

    def test_update_with_valid_location(self):
        location = Location(120, 120, 1)
        trajectory = self.model.update(location)
        self.assertEqual(len(trajectory), 201)
        self.assertIsInstance(trajectory[0], Location)

    def test_update_with_negative_coordinates(self):
        location = Location(-50, -50, 1)
        trajectory = self.model.update(location)
        self.assertEqual(len(trajectory), 201)
        self.assertIsInstance(trajectory[0], Location)

    def test_update_with_out_of_bounds_coordinates(self):
        location = Location(250, 250, 1)
        trajectory = self.model.update(location)
        self.assertEqual(len(trajectory), 201)
        self.assertIsInstance(trajectory[0], Location)

    def test_update_with_zero_coordinates(self):
        location = Location(0, 0, 1)
        trajectory = self.model.update(location)
        self.assertEqual(len(trajectory), 201)
        self.assertIsInstance(trajectory[0], Location)

    def test_calculate_future_location_with_default_params(self):
        trajectory = [Location(100, 100, 0), Location(120, 120, 1)]
        future_location = self.model.calculateFutureLocation(trajectory, 1)
        self.assertIsInstance(future_location, Location)
        self.assertAlmostEqual(future_location.x, 120, delta=0.1)
        self.assertAlmostEqual(future_location.y, 120, delta=0.1)

    def test_calculate_future_location_with_custom_params(self):
        model = Model(self.initial_pos, friction=0.5, x_attraction_force=0.1, y_attraction_force=0.1,
                      board_min_x=50, board_min_y=50, board_max_x=150, board_max_y=150,
                      iterations=100, friction_limit=0.2, attraction_min_speed=0.5)
        trajectory = [Location(100, 100, 0), Location(120, 120, 1)]
        future_location = model.calculateFutureLocation(trajectory, 1)
        self.assertIsInstance(future_location, Location)
        self.assertNotAlmostEqual(future_location.x, 140, delta=0.1)
        self.assertNotAlmostEqual(future_location.y, 140, delta=0.1)

    def test_calculate_future_location_with_boundary_collision(self):
        trajectory = [Location(195, 195, 0), Location(200, 200, 1)]
        future_location = self.model.calculateFutureLocation(trajectory, 1)
        self.assertIsInstance(future_location, Location)
        self.assertLessEqual(future_location.x, 200)
        self.assertLessEqual(future_location.y, 200)
    
    def test_update_with_multiple_locations(self):
        locations = [Location(random.randint(0, 200), random.randint(0, 200), i) for i in range(10)]
        trajectory = self.model.update(locations[0])
        for location in locations[1:]:
            trajectory = self.model.update(location)
        self.assertEqual(len(trajectory), 201)
        self.assertIsInstance(trajectory[0], Location)

    def test_update_with_varying_frame_numbers(self):
        locations = [Location(random.randint(0, 200), random.randint(0, 200), random.randint(0, 100)) for _ in range(10)]
        trajectory = self.model.update(locations[0])
        for location in locations[1:]:
            trajectory = self.model.update(location)
        self.assertEqual(len(trajectory), 201)
        self.assertIsInstance(trajectory[0], Location)

    def test_calculate_future_location_with_zero_velocity(self):
        trajectory = [Location(100, 100, 0), Location(100, 100, 1)]
        future_location = self.model.calculateFutureLocation(trajectory, 1)
        self.assertIsInstance(future_location, Location)
        self.assertAlmostEqual(future_location.x, 100, delta=0.1)
        self.assertAlmostEqual(future_location.y, 100, delta=0.1)

    def test_calculate_future_location_with_max_iterations(self):
        model = Model(self.initial_pos, iterations=1000)
        trajectory = [Location(100, 100, 0), Location(120, 120, 1)]
        future_location = model.calculateFutureLocation(trajectory, 1)
        self.assertIsInstance(future_location, Location)

    def test_model_accuracy(self):
        # Generate random locations for testing
        locations = [Location(random.randint(0, 200), random.randint(0, 200), i) for i in range(100)]
        
        # Update the model with the locations and store the predicted trajectories
        predicted_trajectories = []
        for location in locations:
            predicted_trajectory = self.model.update(location)
            predicted_trajectories.append(predicted_trajectory)
        
        # Calculate the average distance between predicted and actual locations
        total_distance = 0
        for i in range(len(locations) - 1):
            actual_location = locations[i + 1]
            predicted_location = predicted_trajectories[i][-1]
            distance = ((actual_location.x - predicted_location.x) ** 2 +
                        (actual_location.y - predicted_location.y) ** 2) ** 0.5
            total_distance += distance
        
        average_distance = total_distance / (len(locations) - 1)
        
        # Assert that the average distance is within an acceptable threshold
        self.assertLess(average_distance, 10)  # Adjust the threshold as needed

    def test_model_consistency(self):
        # Generate random locations for testing
        locations = [Location(random.randint(0, 200), random.randint(0, 200), i) for i in range(100)]
        
        # Update the model multiple times with the same locations
        trajectories = []
        for _ in range(5):
            trajectory = []
            for location in locations:
                predicted_trajectory = self.model.update(location)
                trajectory.append(predicted_trajectory)
            trajectories.append(trajectory)
        
        # Assert that the predicted trajectories are consistent across multiple runs
        for i in range(1, len(trajectories)):
            self.assertEqual(trajectories[i], trajectories[0])

if __name__ == '__main__':
    unittest.main()