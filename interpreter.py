import time
from agent import Agent
from environment import Environment
from utils import KeyEvent, Stats, logger, LIMIT_DURATION, Action, Game, GameState, Movement
import random
import itertools

from visualize import Visualize
    

class Interpreter:
    def __init__(self) -> None:
        self.exploitation_rate = float(Game.exploit) or 0.0
        self.state = None
        self.next_state = None
        self.current_cell = None
        self.action = None
        self.env = Environment()
        self.ag = Agent()
        if Game.load_path:
            self.ag.load_q_table(Game.load_path)

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
        vertical = [self.env.state[i][x] for i in range(Game.env_size)]
        # return {
        #     Action.UP: ''.join([i[0] for i in itertools.groupby(vertical[y-1::-1])]) \
        #         if vertical[y-1] == 'S' else ''.join(vertical[y-1::-1]),
        #     Action.DOWN: ''.join([i[0] for i in itertools.groupby(vertical[y + 1:])]) \
        #         if vertical[y + 1] == 'S' else ''.join(vertical[y + 1:]),
        #     Action.LEFT: ''.join([i[0] for i in itertools.groupby(self.env.state[y][x-1::-1])]) \
        #          if self.env.state[y][x-1] == 'S' else ''.join(self.env.state[y][x-1::-1]),
        #     Action.RIGHT: ''.join([i[0] for i in itertools.groupby(self.env.state[y][x + 1:])]) \
        #          if self.env.state[y][x + 1] == 'S' else ''.join(self.env.state[y][x + 1:])
        # }
        return {
            Action.UP: ''.join(vertical[y-1::-1]),
            Action.DOWN: ''.join(vertical[y + 1:]),
            Action.LEFT: ''.join(self.env.state[y][x-1::-1]),
            Action.RIGHT: ''.join(self.env.state[y][x + 1:])
        }
        # return {
        #     Action.UP: ''.join([i[0] for i in itertools.groupby(vertical[y-1::-1])]),
        #     Action.DOWN: ''.join([i[0] for i in itertools.groupby(vertical[y + 1:])]),
        #     Action.LEFT: ''.join([i[0] for i in itertools.groupby(self.env.state[y][x-1::-1])]),
        #     Action.RIGHT: ''.join([i[0] for i in itertools.groupby(self.env.state[y][x + 1:])])
        # }
    
    def _send_reward(self) -> None:
        if Game.dontlearn:
            return
        self.ag.update_q_table(self.state, self.next_state, self.action, self._calculate_reward())

    def _request_action(self) -> Action:
        return self.ag.select_action(self.state, self.exploitation_rate)

    def _update_stats(self) -> None:
        if Game.state != GameState.RUNNING:
            Game.state = GameState.RUNNING
            Game.round += 1
            snake_length = len(self.env.snake_position)
            Stats.all_lengths.append(snake_length)
            if snake_length < 10 and self.exploitation_rate > 0.9:
                Game.not_ten += 1
            if self.env.duration > Game.max_duration:
                Game.max_duration = self.env.duration
            if snake_length > Game.max_length:
                Game.max_length = snake_length



            self.env = Environment()
            divider = max(Game.sessions // 10, 1)
            if (Game.round % divider) == 0:
                if Game.sessions >= 10000:
                    logger.info(f'exploit_rate: {self.exploitation_rate:.1f} | max_len: {Game.max_length} | max_dur: {Game.max_duration} | % max_break: {Game.max_break / divider * 100:.2f} | % not_ten: {Game.not_ten / divider * 100:.2f} | qtab_len: {len(self.ag.qtable)}')
                if not Game.dontlearn:
                    self.exploitation_rate += 0.1
                    self.exploitation_rate = 1 if self.exploitation_rate > 0.9 else self.exploitation_rate
                Stats.update_stats()
                Game.reset_stats()
    
    def check_corners_for_G(self) -> bool:
        """
        Checks if the four specified cells contain exactly two 'G' letters.

        Returns:
            bool: True if there are exactly two 'G' letters, False otherwise.
        """
        cells = [
            self.env.state[1][1],
            self.env.state[1][Game.env_size - 2],
            self.env.state[Game.env_size - 2][1],
            self.env.state[Game.env_size - 2][Game.env_size - 2]
        ]
        return cells.count('G') == 2       

    def run(self):
        action_to_function = {
            Action.UP: Movement.move_up,
            Action.DOWN: Movement.move_down,
            Action.LEFT: Movement.move_left,
            Action.RIGHT: Movement.move_right
        }
        if Game.visual:
            visual = Visualize()
        while Game.round != Game.sessions:
            if Game.visual:
                visual.draw_state(self.env.state)
                while True:
                    event = visual.catch_key_event()
                    if event == KeyEvent.EXIT:
                        return
                    if Game.step_by_step and event != KeyEvent.CONTINUE:
                        continue
                    event = visual.catch_key_event()
                    time.sleep(0.2)
                    break
            if self.check_corners_for_G():
                self.exploitation_rate = min(self.exploitation_rate, 0.9)
            else:
                self.exploitation_rate = 1 if Game.exploit else self.exploitation_rate
            self.state = self.next_state or self._get_snake_view()
            self.action = self._request_action()
            self.current_cell = self.env.move(action_to_function[self.action](self.env.snake_position[0]))
            self.next_state = self._get_snake_view() if Game.state == GameState.RUNNING else None
            self._send_reward()
            if self.env.duration > LIMIT_DURATION:
                Game.max_break += 1
                Game.state = GameState.LOST
                self.next_state = None
            self._update_stats()


if __name__ == "__main__":
    random.seed(42)
    play = Interpreter()
    play.run()