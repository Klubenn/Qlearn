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
* add other information to the visual part, like snake length, games played, rates
* log and find situations with extremely long plays, visualize them and find the cause of such behavior
* plot diagramms to display progress
* add saving experiment settings in a file
* add max_duration parameter as an input option
* train long model till the plateau is reached
* implement count of spare moves since last green apple consume and make condition for explore if too long

## Current findings to improve performance
* Squashing snake view to 'SW' for the back view
* Including check for apples in corners and setting exploit rate to 0.9 in that case
* Rounding to int q-table values (Only for dontlearn mode)