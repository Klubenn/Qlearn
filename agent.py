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

    def _initiate_state_weights(self, state):
        if state not in self.qtable:
            self.qtable[state] = {a: 0 for a in Action}
            # TODO think about adding state that has all multiple elements that follow
            # each other (empty cells, apples, snake body) squash into one to make it fit 
            # to the variable size board
    
    def update_q_table(self, state: str, action: Action, reward: int) -> None:
        self.qtable[state][action] = reward  # TODO Bellman equation

    def select_action(self, state: list, exploitation_rate: float):
        explore = random.choices([True, False], [1 - exploitation_rate, exploitation_rate])[0]
        self._initiate_state_weights(state)
        if explore:
            return random.choice([a for a in Action])
        return max(self.qtable, key=self.qtable.get)

