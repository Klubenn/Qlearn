import json
import random
from utils import Action, Settings

class Agent:
    """
    A Q-learning based AI agent for controlling a snake in a grid environment.

    This class implements Q-learning to train the snake to navigate a grid, 
    avoid obstacles, and maximize rewards by consuming green apples while 
    avoiding red apples and walls.

    Attributes:
        qtable (dict): A dictionary mapping states to their Q-values.
        lr (float): Learning rate for Q-learning updates.
        df (float): Discount factor for future rewards.

    Methods:
        select_action(state: dict, exploitation_rate: float) -> Action:
            Selects the next move based on exploration or exploitation.
        update_q_table(state: dict, new_state: dict | None, action: Action, reward: int) -> None:
            Updated Q-values according to Bellman equation.
        _initiate_state_weights(states: dict) -> None:
            Ensures Q-values are initialized for all states.
    """
    def __init__(self) -> None:
        self.qtable = dict()
        self.lr = 0.05
        self.df = 0.9

    def select_action(self, state: dict, exploitation_rate: float) -> Action:
        """
        Selects the direction of the snake's next move based on a balance of exploration and exploitation.

        Args:
            state (dict): A dictionary where:
                - Keys are directions from the `Action` enum (e.g., Action.UP, Action.DOWN, etc.).
                - Values are strings describing what the snake sees in each direction. 
                Each string can include the following:
                    - 'S': Snake's own body.
                    - 'G': Green apple.
                    - 'R': Red apple.
                    - 'W': Wall.
                    - '0': Empty space.
                Example:
                    {
                        Action.UP: "S0G0W",
                        Action.DOWN: "0W",
                        Action.LEFT: "G0SW",
                        Action.RIGHT: "0R0W"
                    }
            exploitation_rate (float): The probability of choosing the best known action (exploitation)
                versus a random action (exploration).

        Returns:
            Action: The selected direction of the move.
        """
        explore = random.choices([True, False], [1 - exploitation_rate, exploitation_rate])[0]
        if not Settings.dontlearn:
            self._initiate_state_weights(state)
        if explore:
            return random.choice([a for a in Action])
        action_weights = {a: int(self.qtable[s]) for a, s in state.items() if s in self.qtable}
        max_value = max(action_weights.values())
        if Settings.fill_zeroes:
            max_actions = [a for a, weight in action_weights.items() if weight == 0]
            if not max_actions:
                max_actions = [a for a, weight in action_weights.items() if weight == max_value]
        else:
            max_actions = [a for a, weight in action_weights.items() if weight == max_value]
        return random.choice(max_actions)

    def update_q_table(self, state: dict, new_state: dict | None, action: Action, reward: int) -> None:
        """
        Updates Q-values according to the selected action, current state, new state and reward using Bellman equation.

        Args:
            state (dict): A dictionary mapping each direction (Action) to the corresponding state string.
            new_state (dict or None): 4 directions of the next snake state with corresponding views according to selected action; None if that was the final step and game ends here.
            action (Action): Selected action for the current snake state.
            reward (int): Reward obtained after moving the snake to the next state.
        
        Returns:
            None
        """
        if new_state:
            maxQ_next = max([self.qtable[s] for s in new_state.values() if s in self.qtable])
        else:
            maxQ_next = 0
        self.qtable[state[action]] = self.qtable[state[action]] + self.lr * (
            reward + self.df * maxQ_next - self.qtable[state[action]])
    
    def save_q_table(self, path: str) -> None:
        """
        Saves the Q-table to a file.

        Args:
            path (str): The path to the file where the Q-table will be saved.

        Returns:
            None
        """
        try:
            with open(path, 'w') as f:
                json.dump(self.qtable, f, indent=4)
        except Exception as e:
            print(f'Error saving Q-table: {e}')

    def load_q_table(self, path: str) -> None:
        """
        Loads the Q-table from a file.

        Args:
            path (str): The path to the file where the Q-table is saved.

        Returns:
            None
        """
        try:
            with open(path, 'r') as f:
                self.qtable = json.load(f)
        except Exception as e:
            print(f'Error loading Q-table: {e}')
            exit(1)
        
    def _initiate_state_weights(self, state: dict) -> None:
        """
        Initializes Q-values for the snake's current state in all possible directions.

        This function ensures that each string, representing the snake's view 
        in a specific direction, has an initial Q-value in the Q-table. If a view string 
        does not already exist in the Q-table, it is initialized with a value of 0.

        Args:
            state (dict): A dictionary mapping each direction (Action) to the corresponding state string.

        Returns:
            None
        """
        for s in state.values():
            if s not in self.qtable:
                self.qtable[s] = 0
