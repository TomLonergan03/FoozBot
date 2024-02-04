class LinearPathFinder:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.m = None
        self.c = None
        self.direction = None

    def compute_line(self):
        # Calculate the means of x and y
        x_mean = sum(x for x, _ in self.coordinates) / len(self.coordinates)
        y_mean = sum(y for _, y in self.coordinates) / len(self.coordinates)

        # Calculate the terms needed for the numerator and denominator of the slope (m)
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in self.coordinates)
        denominator = sum((x - x_mean) ** 2 for x, _ in self.coordinates)

        # Calculate slope (m) and y-intercept (c)
        self.m = numerator / denominator
        self.c = y_mean - self.m * x_mean

        #Calculate direction 
        if len(self.coordinates) > 1:
            start_point = self.coordinates[0]
            end_point = self.coordinates[-1]
            direction_vector = end_point[0] - start_point[0]
            self.direction = 1 if direction_vector > 0 else -1

    def get_line_parameters(self):
        self.compute_line()
        return self.m, self.c, self.direction
    
    def update_coords(self, coord):
        if self.coordinates is None:
            self.coordinates = [coord]
        else:
            if len(self.coordinates) == 5:
                self.coordinates = self.coordinates[1:]
            self.coordinates.append(coord)