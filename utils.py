from collections import namedtuple
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CELL = 50
BOARD_SIZE = 10
MAX_DURATION = 400
SESSIONS = 200

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
        max_duration (int): The maximum duration of a round.
        max_length (int): The maximum length of the snake.
        sessions (int): The number of game sessions to perform.
        boardsize (int): The size of the game board.
        env_size (int): The size of the game environment including walls.
        save_path (str): The path where the model (q-table) will be saved.
        load_path (str): The path where the model (q-table) will be loaded from.
        visual (str): Display training progress ('on' or 'off').
        dontlearn (bool): If True, the model won't update q-table.
        step_by_step (bool): If True, the model will wait for user input after each move.
    """
    round = 0
    state = GameState.RUNNING
    not_ten = 0
    max_duration = 0
    max_length = 0
    sessions = SESSIONS
    boardsize = BOARD_SIZE
    env_size = BOARD_SIZE + 2  # Walls on each of the sides
    save_path = None
    load_path = None
    visual = 'off'
    dontlearn = False
    step_by_step = False
    manual = False

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
    
