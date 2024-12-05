from enum import Enum
import random

class Action(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Agent:
    def __init__(self) -> None:
        self.qtable = dict()
        self.lr = 0.05  # Learning rate
        self.df = 0.9  # Discount factor
    
    def _initiate_state_weights(self, states: dict):
        for state in states.values():
            if state not in self.qtable:
                self.qtable[state] = 0

    def update_q_table(self, states: dict, new_states: dict, action: Action, reward: int) -> None:
        if new_states:
            maxQ_next = max([self.qtable[s] for s in new_states.values() if s in self.qtable])
        else:
            maxQ_next = 0
        # bellman?
        self.qtable[states[action]] = self.qtable[states[action]] + self.lr * (
            reward + self.df * maxQ_next - self.qtable[states[action]])

    def select_action(self, state: dict, exploitation_rate: float):
        explore = random.choices([True, False], [1 - exploitation_rate, exploitation_rate])[0]
        self._initiate_state_weights(state)
        if explore:
            return random.choice([a for a in Action])
        action_weights = {a: self.qtable[s] for a, s in state.items()}
        return max(action_weights, key=action_weights.get)

