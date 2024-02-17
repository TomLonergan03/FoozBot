import cv2
import numpy as np          # Imports?

class Player:     
    _vision : None          # instantiate class for the vision
    _prediction : None      # instantiate class for prediction
                            # All are currently type None until integration happens.
    
    _ball = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]            # Ball coords for present and the predicted next 4 frames
    _coords_max = (100, 100)                                    # Coords of the field
    
    _row_front : None                                           # Preferrably have classes representing each handle
    _row_back : None                                            # Preferrably also store the coordinates each of their players is at.
    
                                                          # Base player class, will handle basic functionality of players and different difficulties can inherit from this class
    def __init__(self, vision : None, prediction : None, front : None, back : None):  # Currently None until integration happens, preferably all separate sections will be classes and functionality will be in callable functions
        """ Handles initialisation as necessary """
        self._vision = vision
        self._prediction = prediction
        self._row_front = front
        self._row_back = back

        # Initialise coordinates for the rows of players?

    def update():
        """ Called every frame to update the all the coordinates """
        _ball = []                                      # Get ball coordinates for the current and next few frames
        _coords_max = (100, 100)                        # Get max coords of field from vision

    def coords_processing():
        """ Processes internal coordinates and tells the actuators what to do """
        # Find if the ball is in front of or behind each row
        # Find the point the ball will intersect with the row
        # Find the nearest player that can go and intercept the ball
        # Return the outputs necessary into both _row_front and _row_back (eg. if the ball is behind the front row but in front of the back row, make front row go horizontal and back row begin intercepting.)
        # If ball is close enough to effective kicking range for the player, also kick the ball
        pass