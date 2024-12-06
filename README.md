# Q-learning algorithm project.
The aim of this project is to teach a snake play the game with the help of Q-learning algorithm.

## Prepare the workspace
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Launch the game
```
python3 main.py
```

## TODOs
* convert board to numpy array, so that it would be faster to get the column for the snake view
* make snake view in terminal according to the task
* add command-line arguments to launch the program
* add saving the model at some point
* add visualization of the training and automatic play
* add other information to the visual part, like snake length, games played, rates
* introduce a Decay Strategy with Exploration Boost and decay rate
* add mode without q-table update
* log and find situations with extremely long plays, visualize them and find the cause of such behavior

