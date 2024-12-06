from collections import namedtuple
from enum import Enum

BOARD_SIZE = 10

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


class Game:
    round = 0
    game_over = 0


class Movement:
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