from abc import ABC, abstractmethod

class PCInterface(ABC):
    @abstractmethod
    def update_ball_position(self, ball_coords, player_intersections: list[float], time):
        pass
    
    @abstractmethod
    def draw_intersections_on_frame(self, frame):
        pass

    @abstractmethod
    def draw_text(self, frame):
        pass