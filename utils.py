from collections import namedtuple
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BOARD_SIZE = 10
MAX_DURATION = 400
ROUNDS = 200

Position = namedtuple('Position', ['x', 'y'])

class Action(Enum):
    """
    An enumeration representing the possible movement directions of the snake.

    Members:
        UP (int): Move up.
        DOWN (int): Move down.
        LEFT (int): Move left.
        RIGHT (int): Move right.
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class GameState(Enum):
    """
    An enumeration representing the possible states of the game.

    Members:
        RUNNING (int): The game is running.
        LOST (int): The game is lost.
        WON (int): The game is won.
    """
    RUNNING = 0
    LOST = 1
    WON = 2

class Game:
    """
    A class to represent the game state and round.

    Attributes:
        round (int): The current round of the game.
        state (GameState): The current state of the game.
        not_ten (int): The number of rounds where the snake length was less than 10.
    """
    round = 0
    state = GameState.RUNNING
    not_ten = 0

class Movement:
    """
    A class containing static methods to move the snake in different 
    directions and return new position.

    Methods:
        move_up(p: Position) -> Position:
            Moves the snake up by one cell.
        
        move_down(p: Position) -> Position:
            Moves the snake down by one cell.
        
        move_left(p: Position) -> Position:
            Moves the snake left by one cell.
        
        move_right(p: Position) -> Position:
            Moves the snake right by one cell.
    """
    @staticmethod
    def move_up(p: Position) -> Position:
        return Position(p.x, p.y - 1)
    
    @staticmethod
    def move_down(p: Position) -> Position:
        return Position(p.x, p.y + 1)
    
    @staticmethod
    def move_left(p: Position) -> Position:
        return Position(p.x - 1, p.y)
    
    @staticmethod
    def move_right(p: Position) -> Position:
        return Position(p.x + 1, p.y)