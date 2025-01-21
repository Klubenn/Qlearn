# Q-learning Algorithm Project

The aim of this project is to teach a snake to play the game using the Q-learning algorithm.

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Training](#training)
- [Evaluation](#evaluation)
- [Research and Considerations](#research-and-considerations)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This project implements a Q-learning algorithm to train a snake to play the classic snake game. There are 2 green apples and 1 red apple. If the snake eats a green apple, it grows by one cell; if it eats a red apple, it shrinks by one cell. If the snake hits the wall or its own body, or if its size reduces to 0 cells, the game ends. The Q-learning algorithm is a model-free reinforcement learning technique that aims to learn the optimal policy for an agent to take actions in an environment to maximize cumulative reward. Specific conditions of the project limit the view of the snake to only the intersection of the row and column where its head is currently located. This means that the snake does not see the whole board or the location of elements that are on other rows/columns than its head. The snake does not remember its previous view and makes the decision on where to move next based exclusively on the current view.

## Setup
To set up the project, clone the repo and follow these steps:

```sh
# Create a virtual environment:
python3 -m venv venv

# Activate the virtual environment:
source venv/bin/activate

# Install the required dependencies:
pip install -r requirements.txt
```

## Usage
To launch the game, run the following command:
```sh
python3 main.py --config path/to/config
```

## Configuration
You can configure the training and game settings using command-line arguments or a configuration file.

### Command-line Arguments
- `--sessions [int]`: The number of training sessions to perform.
- `--save [postfix]`: The name under which the file will be saved, preceded by number of sessions and an underscore, e.g. `100_postfix`, `1k_postfix`
- `--load [path]`: The path where the training will be loaded from.
- `--visual [on|off]`: Display training progress graphically.
- `--dontlearn`: If present, the model won't update the Q-table.
- `--step-by-step`: If present, the model will wait for user input after each move.
- `--manual`: Play the game manually with visualization.
- `--fill-zeroes`: Prioritize filling zero values in the Q-table.
- `--universal`: Train the model to work on any board size.
- `--seed [int]`: Seed for the random number generator.
- `--epochs [int]`: Number of epochs to train the model.

### Configuration File
You can also use a configuration file (e.g., `config.yaml`) to specify the settings. If the `--config` argument is provided, all other command-line arguments will be ignored, and the settings will be taken from the configuration file. Confuguration files for training and testing are provided in the `configs` directory.

Example `config.yaml`:
```yaml
sessions: 1000
boardsize: 15
save: "training"
load: "models/universal/90k_univ"
visual: false
exploit: true
dontlearn: false
step-by-step: false
manual: false
fill-zeroes: false
universal: true
seed: 42
epochs: 10
```

## Training
To train the snake using the standard settings, run the following command:
```sh
python3 main.py --sessions 1000 --save training
```
This will produce a file `1k_training` which contains the Q-table with weights for the 10x10 board.

Initial training should be performed with `exploit: false` (default) so that the training gradually shifts from an exploration to an exploitation strategy. This is achieved in 10 equal steps. The training starts with an exploitation rate equal to 0.0, and every `sessions/10` rounds it increases by 0.1. By the end of the training, the exploitation rate is 0.9.

The next training should be launched by loading the model produced in the previous step, but this time change the parameter value to `exploit: true`. Now all the training is done with an exploitation rate of 1.0.

Nevertheless, exploration is not really important in this implementation as the only positive reward is given for the green apple, and the empty cell has a reward of -1. As all new, not yet visited states get a value of 0, this means that the snake will choose either unknown states or states with an apple in front of it, which leads to some kind of exploration during the training.

Note that the number of training sessions written out to the file name is calculated gradually. This means that if the training loaded file is `100_train` and there were 10 new sessions, the new filename will be `110_train`.

Additionally, any number that is a multiple of 1000 gets `k` instead of `000`, so after `100000` sessions the output will be `100k`.

## Evaluation
To evaluate the trained model, use the following parameter value: `dontlearn: true` and specify the model to be loaded. During evaluation, the Q-table is not updated, and at the end, when using a config file with multiple models, a graph representing the snake's maximum and mean length and the percentage of snakes whose size was less than 10 is displayed.

## Research, Implementation and Considerations
The main challenge of the project was to come up with an idea of what the current state of the snake would be, that could be saved to the Q-table and would allow the snake to make a decision on where to move next. As the snake's view is limited to only 4 directions - up, down, left, right - and it does not see the rest of the board, this state could use only information in the intersection of the row and column of the snake's head. I came up with an idea to map every direction separately, from the snake's head to the wall in every direction (not including the head). Here is an example of how the board view is limited to the snake view and which states for the Q-table are used:
```
# BOARD           # SNAKE VIEW      # STATES
WWWWWWWWWWWW              W         "UP": "OOOOW"
WOOOOOOOOOOW              O         "DOWN": "OOGOOW"
WOOOOOOOOOOW              O         "LEFT": "SSOOROOW"
WOOOOOOOOOOW              O         "RIGHT": "OOW"
WOOOOOOOOOOW              O         
WOOROOSSHOOW      WOOROOSSHOOW      #LEGEND
WOOOOOSOOOOW              O         H - snake's head
WOOOOOOOOOOW              O         S - snake's body
WOOOOOOOGOOW              G         G - green apple
WOOGOOOOOOOW              O         R - red apple
WOOOOOOOOOOW              O         O - empty cell
WWWWWWWWWWWW              W         W - wall
```

One of the aims of the project was to train the snake to reach a length of 10 or more cells, which is why the evaluation graph lists the percentage of small snakes.

One of the possible bonuses for the project was to train a model that would work without additional training on any board size. Such models can be trained with the `universal: true` parameter. The idea behind this approach is a different mapping of the snake's view, which removes any duplicated cell types that follow each other. So if the snake in one direction sees `OOOGOOW`, the view would be squashed to `OGOW`. This approach allows the same model to be used for any board size but results in slightly reduced maximum lengths of the snake compared to the normal mode.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License
This project is licensed under the MIT License.