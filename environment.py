from utils import Game, GameState, Position, BOARD_SIZE
import random


class Environment:
    def __init__(self, board_size=BOARD_SIZE) -> None:
        """
        Initialize the environment with a given board size.
        
        Args:
            board_size (int): Size of the game board (default is BOARD_SIZE)
        """
        self.env_size = board_size + 2  # Walls on each of the sides
        self.duration = 0
        self.state = self._initialize_board()
        self.snake_position = self._initialize_snake()
        self._initialize_apples()

    def move(self, p: Position) -> str:
        """
        Moves the snake head to the new cell and adjusts the environment to the required state.

        Args:
            p (Position): The new position of the snake's head.

        Returns:
            str: The cell type where the snake's head landed.
        """
        x_new, y_new = p.x, p.y
        letter = self.state[y_new][x_new]
        if letter in ['W', 'S'] or (letter == 'R' and len(self.snake_position) == 1):
            Game.state = GameState.LOST
        else:
            if letter in ['0', 'R']:
                tail = self.snake_position.pop()
                self.state[tail.y][tail.x] = '0'
            if letter == 'R':
                tail = self.snake_position.pop()
                self.state[tail.y][tail.x] = '0'
                self._set_apple(1, 'R')
            elif letter == 'G':
                self._set_apple(1, 'G')
            self.snake_position.insert(0, Position(x_new, y_new))
            self.state[y_new][x_new] = 'H'
            if len(self.snake_position) > 1:
                self.state[self.snake_position[1].y][self.snake_position[1].x] = 'S'
        self.duration += 1
        return letter

    def print_env(self) -> None:
        """
        Prints the current state of the environment.
        """
        for row in self.state:
            print(' '.join(row))

    def _initialize_board(self) -> list:
        """
        Sets walls and empty cells.

        Returns:
            list: The initialized board state.
        """
        arr = list([[] for _ in range(self.env_size)])
        for i in range(self.env_size):
            for j in range(self.env_size):
                if i in [0, self.env_size -1] or j in [0, self.env_size -1]:
                    fill = 'W'
                else:
                    fill = '0'
                arr[i].append(fill)
        return arr
   
    def _initialize_snake(self) -> list[Position]:
        """
        Initialize the snake's position on the board.

        Returns:
            list[Position]: List of Position objects representing the snake's position.
        """
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
    
    def _initialize_apples(self) -> None:
        """
        Initialize apples on the board.
        """
        self._set_apple(2, 'G')
        self._set_apple(1, 'R')

    def _set_apple(self, number: int, color: str) -> None:
        """
        Sets apples on the board.

        Args:
            number (int): Number of apples to set.
            color (str): Color of the apples ('R' or 'G').
        """
        for _ in range(number):
            x, y = self._get_empty_cell()
            if Game.state == GameState.RUNNING:
                self.state[y][x] = color

    def _is_empty(self, x, y) -> bool:
        """
        Checks whether the cell is empty.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            bool: True if empty, False if not.
        """
        return self.state[y][x] == '0'
    
    def _get_empty_cell(self) -> Position:
        """
        Returns the coordinates of an empty cell.

        Returns:
            Position: The coordinates of an empty cell.
        """
        empty = [
            Position(x, y) 
            for y, line in enumerate(self.state) 
            for x, _ in enumerate(line) 
            if self.state[y][x] == '0'
            ]
        if len(empty) == 0:
            print("YOU WON!!!!")
            Game.state = GameState.WON
            return None, None
        return random.choice(empty)

