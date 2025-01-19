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
This project implements a Q-learning algorithm to train a snake to play the classic snake game. There are 2 green apples and 1 red apple. If the snake eats the green apple, it grows by one cell, if red - it shrinks by one cell. If the snake hits the wall or it's own body or if it's size reduces to 0 cells, the game ends. The Q-learning algorithm is a model-free reinforcement learning technique that aims to learn the optimal policy for an agent to take actions in an environment to maximize cumulative reward. Specific conditions of the project limit the view of the snake to only intersection of row and column where it's head is currently located. That means that the snake does not see the whole board and location of elements that are on other rows/columns than it's head. The snake does not remember it's previous view and makes the decision on where to move next based exclusively on current view.

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

Initial training should be performed with `exploit: false` (default) so that the training gradually shifts from explore to exploit strategy. That is achieved in 10 equal steps. The training starts with exploitation rate equal to 0.0 and every `sessions/10` rounds it increases by 0.1. By the end of the training the exploitation rate is 0.9.

The next training should be launched loading the model produced in the previous step, but this time change the parameter value to `exploit: true`. Now all the training is done with the exploitation rate 1.0.

Note that the number of training sessions which is written out to the file name is calculated gradually. That means that if the training loaded file `100_train` and there were 10 new sessions, the new filename will be `110_train`.

Besides that all that is a multiple of 1000 gets `k` instead of `000`, so after `100000` sessions the output will be `100k`.

## Evaluation
To evaluate the trained model, use the following parameter value: `dontlearn: true` and specify the model to be loaded. During evaluation the Q-table is not updated and at the end when using config file with multiple models, the graph representing snake maximum and mean length and % of snakes who's size was less than 10 is displayed.

## Research, Implementation and Considerations
The main challenge of the project was to come up with an idea of what the current state of the snake would be, that could be saved to the Q-table and would allow the snake to make a decision on where to move next. As the snake's view is limited to only 4 directions - up, down, left, right - and it does not see the rest of the board, this state could use only information in intersection of row and column of snake's head. I came up with an idea to map every direction separately, from snake's head till the wall of every direction (not including the head). Here is the example, how board view is limited to snake view and which states for the Q-table are used:
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

One of the aims of the project was to train the snake so that it would reach the length of 10 and more cells, that is why in the evaluation graph the % of small snakes is listed.

One of the possible bonuses for the project was to train such a model, that would work without additional training on any board size. Such models can be trained with the `universal: true` parameter. The idea behind that approach is a different mapping of snake's view which removes any duplicated cell types that follow each other. So if the snake in one direction sees `OOOGOOW` the view would be squashed to `OGOW`. This approach allowes to use the same model for any board size, but results in slightly reduced maximum lengths of the snake.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License
This project is licensed under the MIT License.