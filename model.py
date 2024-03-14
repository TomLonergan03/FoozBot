from collections import deque
from dataclasses import dataclass
from typing import List

@dataclass
class Location:
    x: float
    y: float
    time: float

    def copy(self):
        return Location(self.x, self.y, self.time)


class Model:
    def __init__(self, initial_pos: Location, friction: float = 1, x_attraction_force: float = 0, y_attraction_force: float = 0, board_min_x: int = 0, board_min_y: int = 0, board_max_x: int = 200, board_max_y: int = 200, iterations: int = 20, friction_limit: int = 0, attraction_min_speed: int = 0, number_of_averages: int = 10):
        """
        Args:
        initial_pos (Location): Initial position of the ball.
        friction (float, optional): Multiplied with velocity each frame to imitate friction slowing the ball. Defaults to 1.
        x_attraction_force (float, optional): Attraction force in the x axis. Defaults to 0.
        y_attraction_force (float, optional): Attraction force in the y axis. Defaults to 0.
        board_min_x (int, optional): Minimum x value the ball can take. Defaults to 0.
        board_min_y (int, optional): Minimum y value the ball can take. Defaults to 0.
        board_max_x (int, optional): Maximum x value the ball can take. Defaults to 200.
        board_max_y (int, optional): Maximum y value the ball can take. Defaults to 200.
        iterations (int, optional): Number of iterations to predict the future. Defaults to 20.
        friction_limit (int, optional): Minimum speed for friction to occur. Defaults to 0.
        attraction_min_speed (int, optional): Minimum speed for attraction to occur. Defaults to 0.
        number_of_averages (int, optional): Number of averages to calculate the future. Defaults to 10.
        """
        self.history = deque(maxlen=2)
        self.history.append(initial_pos)
        self.friction = 1 - friction
        self.x_attraction_force = x_attraction_force
        self.y_attraction_force = y_attraction_force
        self.board_max_x = board_max_x
        self.board_max_y = board_max_y
        self.board_min_x = board_min_x
        self.board_min_y = board_min_y
        self.prediction = initial_pos
        self.iterations = iterations
        self.friction_limit = friction_limit
        self.attraction_min_speed = attraction_min_speed
        self.futures = deque(maxlen=number_of_averages)

    def update(self, location: Location) -> List[Location]:
        """
        Predicts the future path of the ball.
        Args:
        location (Location): The current location of the ball.
        Returns:
        List[Location]: A list of the future locations of the ball.
        """
        location = Location((location.x + self.prediction.x) / 2,
                            (location.y + self.prediction.y) / 2, location.time)
        self.history.append(
            Location(location.x, location.y, location.time))
        future = []
        future.extend(self.history)
        for _ in range(self.iterations):
            future.append(self.calculateFutureLocation(
                future, 1))
        self.prediction = future[2]
        trajectory = [location] + future[2:]
        self.futures.append(trajectory)
        avg = [] * len(self.futures[0])
        for frame_number in range(len(self.futures[0])):
            avg.append(Location(0, 0, 0))
        for future in self.futures:
            for frame_number in range(len(future)):
                avg[frame_number] = Location(avg[frame_number].x + future[frame_number].x,
                                             avg[frame_number].y + future[frame_number].y, future[frame_number].time)
        for av in avg:
            av.x = av.x / len(self.futures)
            av.y = av.y / len(self.futures)
        return avg

    def calculateFutureLocation(self, trajectory: List[Location], time: float) -> Location:
        """
        Calculates the next location of the ball based on a trajectory.
        Args:
        trajectory (List[Location]): The past (real or predicted) trajectory of the ball.
        time (float): The time between the current and desired next location.
        Returns:
        Location: The next location of the ball.
        """
        dx = (trajectory[-1].x - trajectory[-2].x) / \
            (trajectory[-1].time - trajectory[-2].time)
        dy = (trajectory[-1].y - trajectory[-2].y) / \
            (trajectory[-1].time - trajectory[-2].time)

        if abs(dx) > self.attraction_min_speed:
            dx -= (trajectory[-1].x - (self.board_max_x -
                                       self.board_min_x) / 2) * self.x_attraction_force
        if abs(dy) > self.attraction_min_speed:
            dy -= (trajectory[-1].y - (self.board_max_y -
                                       self.board_min_y) / 2) * self.y_attraction_force

        # friction
        if abs(dx) > self.friction_limit:
            dx *= self.friction
        if abs(dy) > self.friction_limit:
            dy *= self.friction

        new_location = Location(
            trajectory[-1].x + dx * time, trajectory[-1].y + dy * time, trajectory[-1].time + time)

        if new_location.x >= self.board_max_x:
            dx = -dx
            new_location.x = self.board_max_x + dx * time
        elif new_location.x <= self.board_min_x:
            dx = -dx
            new_location.x = self.board_min_x + dx * time
        if new_location.y >= self.board_max_y:
            dy = -dy
            new_location.y = self.board_max_y + dy * time
        elif new_location.y <= self.board_min_y:
            dy = -dy
            new_location.y = self.board_min_y + dy * time
        return new_location
