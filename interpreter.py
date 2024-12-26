import time
from agent import Agent
from environment import Environment
from utils import KeyEvent, Settings, Stats, logger, LIMIT_DURATION, Action, Step, GameState, Movement
import random
import itertools

from visualize import Visualize
    

class Interpreter:
    def __init__(self) -> None:
        self.exploitation_rate = float(Settings.exploit) or 0.0
        self.state = None
        self.next_state = None
        self.current_cell = None
        self.action = None
        self.env = Environment()
        self.ag = Agent()
        if Settings.load_path:
            self.ag.load_q_table(Settings.load_path)

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
        vertical = [self.env.state[i][x] for i in range(Settings.env_size)]
        if Settings.train_universal:
            return {
                Action.UP: ''.join([i[0] for i in itertools.groupby(vertical[y-1::-1])]),
                Action.DOWN: ''.join([i[0] for i in itertools.groupby(vertical[y + 1:])]),
                Action.LEFT: ''.join([i[0] for i in itertools.groupby(self.env.state[y][x-1::-1])]),
                Action.RIGHT: ''.join([i[0] for i in itertools.groupby(self.env.state[y][x + 1:])])
            }
        return {
            Action.UP: ''.join(vertical[y-1::-1]),
            Action.DOWN: ''.join(vertical[y + 1:]),
            Action.LEFT: ''.join(self.env.state[y][x-1::-1]),
            Action.RIGHT: ''.join(self.env.state[y][x + 1:])
        }
        
    def _send_reward(self) -> None:
        if Settings.dontlearn:
            return
        self.ag.update_q_table(self.state, self.next_state, self.action, self._calculate_reward())

    def _request_action(self) -> Action:
        return self.ag.select_action(self.state, self.exploitation_rate)

    def _update_stats(self) -> None:
        if Step.state != GameState.RUNNING:
            Step.state = GameState.RUNNING
            Stats.round += 1
            snake_length = len(self.env.snake_position)
            Stats.all_lengths.append(snake_length)
            if snake_length < 10:
                Step.not_ten += 1
            if self.env.duration > Step.max_duration:
                Step.max_duration = self.env.duration
            if snake_length > Step.max_length:
                Step.max_length = snake_length

            self.env = Environment()
            divider = max(Settings.sessions // 10, 1)
            if (Stats.round % divider) == 0:
                if Settings.sessions >= 10000:
                    logger.info(f'exploit_rate: {self.exploitation_rate:.1f} | max_len: {Step.max_length} | max_dur: {Step.max_duration} | % breaks: {Step.max_break / divider * 100:.2f} | % not_ten: {Step.not_ten / divider * 100:.2f} | qtab_len: {len(self.ag.qtable)}')
                if not Settings.dontlearn:
                    self.exploitation_rate += 0.1
                    self.exploitation_rate = 1 if self.exploitation_rate > 0.9 else self.exploitation_rate
                Stats.update_stats()
                Step.reset_stats()
    
    def run(self):
        action_to_function = {
            Action.UP: Movement.move_up,
            Action.DOWN: Movement.move_down,
            Action.LEFT: Movement.move_left,
            Action.RIGHT: Movement.move_right
        }
        if Settings.visual:
            visual = Visualize()
        while Stats.round != Settings.sessions:
            if Settings.visual:
                visual.draw_state(self.env.state)
                while True:
                    event = visual.catch_key_event()
                    if event == KeyEvent.EXIT:
                        return
                    if Settings.step_by_step and event != KeyEvent.CONTINUE:
                        continue
                    time.sleep(0.2)
                    break
            self.state = self.next_state or self._get_snake_view()
            self.action = self._request_action()
            self.current_cell = self.env.move(action_to_function[self.action](self.env.snake_position[0]))
            self.next_state = self._get_snake_view() if Step.state == GameState.RUNNING else None
            self._send_reward()
            if self.env.duration > LIMIT_DURATION:
                Step.max_break += 1
                Step.state = GameState.LOST
                self.next_state = None
            self._update_stats()


if __name__ == "__main__":
    random.seed(42)
    play = Interpreter()
    play.run()