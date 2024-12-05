"""
Here the full map is present, but the information, that is passed to the interpreter,
is limited only to the snake view
"""

from collections import namedtuple
import random

"""
ACTIONS = UP, DOWN, LEFT, RIGHT
STATE = ['W','0','0','0','0','0','0','0','0','H','W','W','0','0','G','R','0','0','0','H','S','0','W'] # LEFT->RIGHT, UP->DOWN

• W = Wall
• H = Snake Head
• S = Snake body segment
• G = Green apple
• R = Red apple
• 0 = Empty space
"""

BOARD_SIZE = 10
Position = namedtuple('Position', ['x', 'y'])


class Environment:
    def __init__(self, board_size=BOARD_SIZE) -> None:
        self.board_size = board_size
        self.env_size = self.board_size + 2  # Walls on each of the sides
        self.state = self.set_blank_board()
        self.snake_position = self.set_snake()
        self.duration = 0
        self.set_apple(2, 'G')
        self.set_apple(1, 'R')

    def set_blank_board(self) -> list:
        """Sets walls and empty cells."""
        arr = list([[] for _ in range(self.env_size)])
        for i in range(self.env_size):
            for j in range(self.env_size):
                if i in [0, self.env_size -1] or j in [0, self.env_size -1]:
                    fill = 'W'
                else:
                    fill = '0'
                arr[i].append(fill)
        return arr
   
    def set_snake(self) -> list[Position]:
        self.snake_position = []
        
        # Set snake head
        x, y = self._get_empty_cell()
        self.state[y][x] = 'H'
        snake_position = [Position(x, y)]
        
        # Set snake body
        for _ in range(2):
            while True:
                x_new, y_new = random.choice([(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)])
                if self._is_empty(x_new, y_new):
                    x, y = x_new, y_new
                    self.state[y][x] = 'S'
                    snake_position.append(Position(x, y))
                    break

        return snake_position

    def set_apple(self, number: int, color: str) -> None:
        assert color in ['R', 'G'], "Unknown apple color"
        for _ in range(number):
            x, y = self._get_empty_cell()
            if Game.game_over == 1:
                return
            self.state[y][x] = color

    def move(self, p: Position) -> str:
        """ Moves the snake head to the new cell and adjusts the environment 
            to the required state.

            Returns:
                str: cell type, where the snake's head landed
        """
        x_new, y_new = p.x, p.y
        letter = self.state[y_new][x_new]
        if letter in ['W', 'S'] or (letter == 'R' and len(self.snake_position) == 1):
            Game.game_over = 1
        else:
            if letter in ['0', 'R']:
                self.state[self.snake_position[-1].y][self.snake_position[-1].x] = '0'
                self.snake_position = self.snake_position[:-1]
            if letter == 'R':
                self.state[self.snake_position[-1].y][self.snake_position[-1].x] = '0'
                self.snake_position = self.snake_position[:-1]
                self.set_apple(1, 'R')
            elif letter == 'G':
                self.set_apple(1, 'G')
            self.snake_position.insert(0, Position(x_new, y_new))
            self.state[y_new][x_new] = 'H'
            if len(self.snake_position) > 1:
                self.state[self.snake_position[1].y][self.snake_position[1].x] = 'S'
        self.duration += 1
        return letter

    def print_env(self) -> None:
        for row in self.state:
            print(' '.join(row))

    def _is_empty(self, x, y) -> bool:
        """Checks whether the cell is empty.

        Returns: True if empty, False if not
        """
        return self.state[y][x] == '0'
    
    def _get_empty_cell(self) -> Position:
        """Returnes the coordinates of an empty cell."""
        while True:
            empty = [
                Position(x, y) 
                for y, line in enumerate(self.state) 
                for x, _ in enumerate(line) 
                if self.state[y][x] == '0'
                ]
            if len(empty) == 0:
                print("YOU WON!!!!")
                Game.game_over = 1
                return None, None
            return random.choice(empty)


class Game:
    round = 0
    game_over = 0
