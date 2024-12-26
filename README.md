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
* make snake view in terminal according to the task
* add other information to the visual part, like snake length, games played, rates
* plot diagramms to display progress
* add saving experiment settings in a file
* Remove from saved training all occurences of `^\s{4}"S.*: 0,$` - maybe insert in code?
* Add matplotlib to visualize model evaluation results
