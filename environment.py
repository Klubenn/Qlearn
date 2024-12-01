"""
Here the full map is present, but the information, that is passed to the interpreter,
is limited only to the snake view
"""

import interpreter
import numpy as np
import pandas as pd
import random

from agent import Movement
"""
ACTIONS = UP, DOWN, LEFT, RIGHT
ARBITRARY_STATE = [W,0,0,0,0,0,0,0,0,H,W,W,0,0,G,R,0,0,0,H,S,0,W] # LEFT->RIGHT, UP->DOWN

• W = Wall
• H = Snake Head
• S = Snake body segment
• G = Green apple
• R = Red apple
• 0 = Empty space
"""

BOARD_SIZE = 10


class Environment:
    def __init__(self, board_size=None) -> None:
        self.board_size = board_size or BOARD_SIZE
        self.env_size = self.board_size + 2  # Walls on each of the sides
        self.state = self.set_blank_board()
        self.set_snake()
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
   
    def set_snake(self):
        # Set snake head
        hor, ver = self._get_empty_cell()
        self.state[hor][ver] = 'H'
        
        # Set snake body
        for _ in range(2):
            while True:
                hor_new, ver_new = random.choice([Movement.move_up(hor, ver), 
                                                  Movement.move_down(hor, ver), 
                                                  Movement.move_left(hor, ver), 
                                                  Movement.move_right(hor, ver)])
                if self._is_empty(hor_new, ver_new):
                    hor, ver = hor_new, ver_new
                    self.state[hor][ver] = 'S'
                    break

    def set_apple(self, number: int, color: str) -> None:
        for _ in range(number):
            hor, ver = self._get_empty_cell()
            self.state[hor][ver] = color

    def print_env(self) -> None:
        for row in self.state:
            print(' '.join(row))


    def _is_empty(self, hor, ver) -> bool:
        """Checks whether the cell is empty.

        Returns: True if empty, False if not
        """
        return self.state[hor][ver] == '0'
    
    def _get_empty_cell(self) -> tuple:
        """Returnes the coordinates of an empty cell."""
        while True:
            hor, ver = random.randint(1, self.board_size), random.randint(1, self.board_size)
            if self._is_empty(hor, ver):
                return hor, ver



env = Environment()
env.print_env()