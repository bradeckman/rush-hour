#################################################################
# FILE : game.py
# WRITER : Brad Eckman , eckmanbrad , 328958244
# EXERCISE : intro2cse ex9 2020
# DESCRIPTION: The Game class (used as part of the Rush Hour game).
# STUDENTS I DISCUSSED THE EXERCISE WITH: Naftali Arnold
# WEB PAGES I USED: None
# NOTES: See notes in car.py file.
#################################################################


from car import Car
from board import Board
import helper
import sys

# Note: Although these variables are relevant only within the Game class, the
# exercise specifically states not to use methods and variables outside of a
# class that aren't a part of the API. I've taken these out of the Game class
# to filter out any JSON data that does not comply with our restrictions (as
# the exercise also specifies that we must pass a full Board to Game).
CAR_LENGTHS = range(2, 5)
CAR_NAMES = 'YBOGWR'
CAR_ORIENTATIONS = 0, 1
CAR_DIRECTIONS = 'udrl'


class Game:
    """
    The Game class represents an object that contains a Board instance. It
    essentially controls under what rules the Board and it's components will
    operate. This class is also responsible for interacting with the user.
    """
    END_GAME_CHAR, SEP_CHAR = '!', ','
    CAR_LENGTHS = CAR_LENGTHS
    CAR_NAMES = CAR_NAMES
    CAR_ORIENTATIONS = CAR_ORIENTATIONS
    UP, DOWN, RIGHT, LEFT = 'udrl'
    CAR_DIRECTIONS = CAR_DIRECTIONS
    DIRECTIONS_DICT = {UP: 'up', DOWN: 'down', RIGHT: 'right', LEFT: 'left'}

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.board = board

    def __invalid_input(self, user_input):
        """
        Determines if the user's input is valid; prints appropriate message.
        :param user_input: The string received from the user.
        :return: True if invalid, else False
        """
        # Invalid format
        if len(user_input) != 3 or user_input[1] != Game.SEP_CHAR or \
                user_input.count(self.SEP_CHAR) != 1:
            print("Illegal format entered; Try again!")
            return True

        car, direction = user_input.split(self.SEP_CHAR)

        # Check car
        if len(car) != 1 or car not in self.CAR_NAMES:
            print("Illegal car entered; Try again!")
            return True
        # Check direction
        if len(direction) != 1 or direction not in self.CAR_DIRECTIONS:
            print("Illegal direction entered; Try again!")
            return True

        return False

    def __get_input(self):
        """
        Gets input from user.
        :return: The name of the car and the requested direction to move
        """
        user_input = input("Enter your move (car,direction): ")
        # User has selected to end game
        if user_input == self.END_GAME_CHAR:
            print("Goodbye!")
            sys.exit()
        # Make sure input is valid
        while self.__invalid_input(user_input):
            user_input = input("Enter your move (car,direction): ")

        car, direction = user_input.split(self.SEP_CHAR)

        return car, direction

    def __single_turn(self):
        """ Handles gameplay required for a single turn in the game. """
        print(self.board)

        car, direction = self.__get_input()

        # Attempt move, and print appropriate message
        if self.board.move_car(car, direction):
            print("You moved the '" + car + "' car " +
                  self.DIRECTIONS_DICT[direction])
        else:
            print("Unable to move the '" + car + "' car " +
                  self.DIRECTIONS_DICT[direction] + ". Try again!")

    def __game_in_progress(self):
        """
        Checks if the game is still in progress.
        :return: True if game still in progress, else False
        """
        # When there is a Car in the board that is in the target cell and is
        # horizontal, the game is over
        if self.board.cell_content(self.board.target_location()):
            return False

        return True

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print("\n\tWelcome to Rush Hour!\n"
              "Your goal is to reach the star.\n")

        while self.__game_in_progress():
            self.__single_turn()

        print("Nice! You won the game!")


def load_cars_to_board(cars_dict, board):
    """
    Loads cars from dictionary to board, taking into account the Game's
    restrictions.
    :param board: A Board object (see API)
    :param cars_dict: A dict, of format {car_name: length, location, orient.}
    :return: None
    """
    for name, values in cars_dict.items():

        # Check values from json
        if len(values) != 3:
            continue

        length, location, orientation = values  # now we can unpack safely

        # Check location
        if len(location) != 2 and type(location) != list:
            continue
        # Check name
        if name not in CAR_NAMES:
            continue
        # Check length
        if length not in CAR_LENGTHS:
            continue
        # Check orientation
        if orientation not in CAR_ORIENTATIONS:
            continue

        new_car = Car(name, length, tuple(location), orientation)
        board.add_car(new_car)


if __name__ == "__main__":
    """ The main driver for the program. """
    # Create board object
    board = Board()
    # Retrieve car data and load cars to board
    cars_dict = helper.load_json(sys.argv[1])
    load_cars_to_board(cars_dict, board)
    # Create game object, and play
    game = Game(board)
    game.play()
