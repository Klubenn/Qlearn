# Q-learning Algorithm Project

The aim of this project is to teach a snake to play the game using the Q-learning algorithm.

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Training](#training)
- [Evaluation](#evaluation)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This project implements a Q-learning algorithm to train a snake to play the classic snake game. The Q-learning algorithm is a model-free reinforcement learning technique that aims to learn the optimal policy for an agent to take actions in an environment to maximize cumulative reward.

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
To train the snake using the Q-learning algorithm using the standard settings, run the following command:
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

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

## License
This project is licensed under the MIT License.