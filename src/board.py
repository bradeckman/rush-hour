#################################################################
# FILE : board.py
# WRITER : Brad Eckman , eckmanbrad , 328958244
# EXERCISE : intro2cse ex9 2020
# DESCRIPTION: The Board class (used as part of the Rush Hour game).
# STUDENTS I DISCUSSED THE EXERCISE WITH: Naftali Arnold
# WEB PAGES I USED: None
# NOTES: See notes in car.py file.
#################################################################


class Board:
    """
    The Board class represents an object that has a height and width, a defined
    target cell, and a list of Car objects (see API) . A Board instance serves
    as an environment in which Car objects can co-exist and become aware of
    one another.
    """
    EMPTY_CELL, STAR, SPACES, NEWLINE, TAB = '-', '*', '  ', '\n', '\t'
    HEIGHT, WIDTH = 7, 7
    TARGET_CELL = (3, 7)
    ROW, COL = 0, 1

    def __init__(self):
        self.__height = self.HEIGHT
        self.__width = self.WIDTH
        self.__target_cell = Board.TARGET_CELL
        self.cars = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # Initialize 2D list of lists, containing empty cells
        current_board = [[self.EMPTY_CELL for i in range(self.__width)]
                         for j in range(self.__height)]

        # Nested for loops to access individual cells
        for i in range(self.__height):
            for j in range(self.__width):
                # Don't forget target cell
                if (i, j + 1) == self.__target_cell:
                    current_board[i].append(self.STAR)
                # Iterate over cars in board; add name in appropriate cells
                for car in self.cars.values():
                    car_coordinates = car.car_coordinates()
                    if (i, j) in car_coordinates:
                        current_board[i][j] = car.get_name()

        # Format as string, add aesthetic touches
        for i in range(len(current_board)):
            current_board[i] = self.TAB + self.SPACES.join(current_board[i])
        current_board = self.NEWLINE.join(current_board)

        return current_board

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        cells = []
        row_of_target, col_before_target = self.__target_cell[Board.ROW], \
                                           self.__target_cell[Board.COL] - 1

        for i in range(self.__height):
            for j in range(self.__width):
                cells.append((i, j))
                # Don't forget to add target cell
                if i == row_of_target and j == col_before_target:
                    cells.append(self.__target_cell)

        return cells

    def __invalid_cell(self, cell):
        """
        Checks if a cell is a 'valid' cell.
        :param cell: A tuple of coordinates (row, col)
        :return: True if invalid, else False
        """
        # A cell is invalid if: 1) it is not on the board, or 2) it is not
        # empty, i.e another car object is already there
        if cell not in self.cell_list() or self.cell_content(cell) is not None:
            return True

        return False

    def __valid_adjacent_cells(self, car, direction):
        """
        Checks if all cells required to make a move are valid.
        :param car: A car object (see API)
        :param direction: The requested direction to move
        :return: True if cells are valid, else False
        """
        for cell in car.movement_requirements(direction):
            if self.__invalid_cell(cell):
                return False

        return True

    def possible_moves(self):
        """
        This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name, movekey, description)
                 representing legal moves
        """
        possible_moves = []
        # Iterate over cars on board; if all locations required to make a move
        # for the given car are valid, add to possible_moves
        for name, car in self.cars.items():
            for direction, desc in car.possible_moves().items():
                if self.__valid_adjacent_cells(car, direction):
                    possible_moves.append((name, direction, desc))

        return possible_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be
        filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return self.__target_cell

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        for name, car in self.cars.items():
            if coordinate in car.car_coordinates():
                return name

        return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Don't add cars that have the same name as an existing car
        if car.get_name() in self.cars:
            return False
        # Don't add cars with invalid locations
        for cell in car.car_coordinates():
            if self.__invalid_cell(cell):
                return False

        # Add the self.cars dictionary
        self.cars[car.get_name()] = car

        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # Check if car with name 'name' exists in board
        if name not in self.cars:
            return False
        # Retrieve appropriate car object
        car = self.cars[name]
        # Don't move if required cells for move are invalid
        for cell in car.movement_requirements(movekey):
            if self.__invalid_cell(cell):
                return False

        if car.move(movekey):
            return True

        return False
