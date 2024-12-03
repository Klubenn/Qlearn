from agent import Agent, Action
from environment import Environment, Game, Position
import random

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
    
action_to_function = {
    Action.UP: Movement.move_up,
    Action.DOWN: Movement.move_down,
    Action.LEFT: Movement.move_left,
    Action.RIGHT: Movement.move_right
}

class Interpreter:
    def __init__(self, exploitation=False) -> None:
        self.exploitation_rate = float(exploitation is True) or 0.0
        self.state = None
        self.current_cell = None
        self.action = None
        self.max_length = 0
        self.max_duration = 0
        self.env = Environment()
        self.ag = Agent()

    def _calculate_reward(self):
        if self.current_cell in ['W', 'H', 'S']:
            return -100
        elif self.current_cell == 'R':
            return -10
        elif self.current_cell == '0':
            return -1
        elif self.current_cell == 'G':
            return 10

    def _get_snake_view(self) -> list:
        x, y = self.env.snake_position[0]
        view = self.env.state[y] + [self.env.state[i][x] for i in range(self.env.env_size)]
        return ''.join(view)
    
    def _send_reward(self) -> None:
        self.ag.update_q_table(self.state, self.action, self._calculate_reward())

    def _request_action(self) -> Action:
        return self.ag.select_action(self.state, self.exploitation_rate)

    def _update_stats(self) -> None:
        if Game.game_over == 1:
            Game.round += 1
            Game.game_over = 0
            if self.env.duration > self.max_duration:
                self.max_duration = self.env.duration
            if (snake_length := len(self.env.snake_position)) > self.max_length:
                self.max_length = snake_length
            # print("Game over")
            # print(f"Snake length: {snake_length}")
            # print(f"Rounds played: {Game.round}")
            self.env = Environment()
            if Game.round % 10000 == 0:
                self.exploitation_rate -= 0.1
                self.exploitation_rate = 0 if self.exploitation_rate < 0 else self.exploitation_rate
                print(f'Max length: {self.max_length}')
                print(f'Max duration: {self.max_duration}')
                print(len(self.ag.qtable))


    def run(self):
        while True:
            self.state = self._get_snake_view()
            self.action = self._request_action()
            self.current_cell = self.env.move(action_to_function[self.action](self.env.snake_position[0]))
            self._send_reward()
            self._update_stats()
            
            if Game.round % 100000 == 0:
                break


if __name__ == "__main__":
    random.seed(42)
    play = Interpreter()
    play.run()