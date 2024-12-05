from agent import Agent, Action
from environment import Environment, Game, Position
import random
import itertools

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
        self.next_state = None
        self.current_cell = None
        self.action = None
        self.max_length = 0
        self.max_duration = 0
        self.env = Environment()
        self.ag = Agent()

    def _calculate_reward(self) -> int:

        if self.current_cell in ['W', 'S']:
            return -100
        elif self.current_cell == 'R':
            return -10
        elif self.current_cell == '0':
            return -1
        elif self.current_cell == 'G':
            return 20
    
    def _get_snake_view(self) -> dict:
        x, y = self.env.snake_position[0]
        vertical = [self.env.state[i][x] for i in range(self.env.env_size)]
        return {
            Action.UP: ''.join([i[0] for i in itertools.groupby(vertical[y-1::-1])]),
            Action.DOWN: ''.join([i[0] for i in itertools.groupby(vertical[y + 1:])]),
            Action.LEFT: ''.join([i[0] for i in itertools.groupby(self.env.state[y][x-1::-1])]),
            Action.RIGHT: ''.join([i[0] for i in itertools.groupby(self.env.state[y][x + 1:])])
        }
    
    def _send_reward(self) -> None:
        self.ag.update_q_table(self.state, self.next_state, self.action, self._calculate_reward())

    def _request_action(self) -> Action:
        return self.ag.select_action(self.state, self.exploitation_rate)

    def _update_stats(self) -> None:
        if Game.game_over == 1:
            if (Game.round > 99980 and Game.round < 100030):
                print(f'len: {len(self.env.snake_position)} | dur: {self.env.duration}')
            Game.round += 1
            Game.game_over = 0
            if self.env.duration > self.max_duration:
                self.max_duration = self.env.duration
            if (snake_length := len(self.env.snake_position)) > self.max_length:
                self.max_length = snake_length

            self.env = Environment()
            if Game.round % 10000 == 0:
                print(f'exploit_rate: {self.exploitation_rate} | max_len: {self.max_length} | max_dur: {self.max_duration} | qtab_len: {len(self.ag.qtable)}')
                self.exploitation_rate += 0.1
                self.exploitation_rate = 0.8 if self.exploitation_rate > 1 else self.exploitation_rate
                self.max_duration, self.max_length = 0, 0
            


    def run(self):
        while True:
            self.state = self.next_state or self._get_snake_view()
            self.action = self._request_action()
            self.current_cell = self.env.move(action_to_function[self.action](self.env.snake_position[0]))
            if not Game.game_over:
                self.next_state = self._get_snake_view()
            else:
                self.next_state = None
            self._send_reward()
            if self.env.duration > 200:
                Game.game_over = 1
                self.next_state = None
            self._update_stats()
            
            if Game.round % 150000 == 0:
                print("Some values from Q-table:")
                for i, (k, v) in enumerate(self.ag.qtable.items()):
                    print(f"{k}: {v}")
                    if i == 20:
                        break
                break


if __name__ == "__main__":
    random.seed(42)
    play = Interpreter()
    play.run()