#################################################################
# FILE : car.py
# WRITER : Brad Eckman , eckmanbrad , 328958244
# EXERCISE : intro2cse ex9 2020
# DESCRIPTION: The Car class (used as part of the Rush Hour game).
# STUDENTS I DISCUSSED THE EXERCISE WITH: Naftali Arnold
# WEB PAGES I USED: None
# NOTES: It was challenging to understand how our code will be graded, and I
# therefore chose to be conservative on my access to variables/methods, as well
# as testing user input.
#################################################################


class Car:
    """
    The Car class represents an object that has a name, length, location and
    orientation. Each Car instance can move in one of 4 directions - up, down,
    right and left.
    """
    UP, DOWN, RIGHT, LEFT = 'udrl'
    VERTICAL, HORIZONTAL = ORIENTATIONS = ROW, COL = 0, 1
    HEAD_INDEX, TRUNK_INDEX = 0, -1

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col)
                         location
        :param orientation: 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        coordinates = []
        spacer = 0

        # Iterate and adds cell (represented as tuple (row, col))
        for i in range(self.__length):

            if self.__orientation == self.VERTICAL:
                coordinates.append((self.__location[self.ROW] + spacer,
                                    self.__location[self.COL]))
            if self.__orientation == self.HORIZONTAL:
                coordinates.append((self.__location[self.ROW],
                                    self.__location[self.COL] + spacer))
            spacer += 1

        return coordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
        permitted by this car.
        """
        vertical_dict = {self.UP: 'Vertically move the car 1 space upwards',
                         self.DOWN: 'Vertically move the car 1 space '
                                    'downwards'}

        horizontal_dict = {self.RIGHT: 'Horizontally move the car 1 space to '
                                       'the right',
                           self.LEFT: 'Horizontally move the car 1 space to '
                                      'the left'}

        if self.__orientation == self.VERTICAL:
            return vertical_dict
        if self.__orientation == self.HORIZONTAL:
            return horizontal_dict

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this
                 move to be legal.
        """
        requirements = []

        # Add appropriate cells
        if movekey == Car.UP:
            trailing_cell = self.car_coordinates()[self.HEAD_INDEX]
            requirements.append((trailing_cell[self.ROW] - 1,
                                 trailing_cell[self.COL]))
        if movekey == Car.DOWN:
            trailing_cell = self.car_coordinates()[self.TRUNK_INDEX]
            requirements.append((trailing_cell[self.ROW] + 1,
                                 trailing_cell[self.COL]))
        if movekey == Car.RIGHT:
            trailing_cell = self.car_coordinates()[self.TRUNK_INDEX]
            requirements.append((trailing_cell[self.ROW],
                                 trailing_cell[self.COL] + 1))
        if movekey == Car.LEFT:
            trailing_cell = self.car_coordinates()[self.HEAD_INDEX]
            requirements.append((trailing_cell[self.ROW],
                                 trailing_cell[self.COL] - 1))

        return requirements

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        # Do not move if orientation does now allow a move in that direction
        if movekey not in self.possible_moves():
            return False

        # Move in appropriate direction
        if movekey == self.UP:
            self.__location = (self.__location[self.ROW] - 1,
                               self.__location[self.COL])
        if movekey == self.DOWN:
            self.__location = (self.__location[self.ROW] + 1,
                               self.__location[self.COL])
        if movekey == self.RIGHT:
            self.__location = (self.__location[self.ROW],
                               self.__location[self.COL] + 1)
        if movekey == self.LEFT:
            self.__location = (self.__location[self.ROW],
                               self.__location[self.COL] - 1)

        return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
