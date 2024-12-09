import argparse
import random
from interpreter import Interpreter
from utils import Game
from visualize import Visualize

def parse_arguments():
    parser = argparse.ArgumentParser(description="Train a snake game AI model.")
    parser.add_argument('--sessions', type=int, default=10, help='The number of training sessions to perform')
    parser.add_argument('--boardsize', type=int, default=10, help='The size of the board')
    parser.add_argument('--save', type=str, help='The path where the result of the training will be saved')
    parser.add_argument('--load', type=str, help='The path where the training will be loaded from')
    parser.add_argument('--visual', choices=['on', 'off'], default='off', help='Display training progress')
    parser.add_argument('--dontlearn', action='store_true', help="If present, the model won't update q-table")
    parser.add_argument('--step-by-step', action='store_true', help='If present, the model will wait for user input after each move')
    parser.add_argument('--manual', action='store_true', help='Play the game manually')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Set the Game class attributes
    Game.sessions = args.sessions
    Game.boardsize = args.boardsize
    Game.env_size = args.boardsize + 2
    Game.save_path = args.save
    Game.load_path = args.load
    Game.visual = args.visual
    Game.dontlearn = args.dontlearn
    Game.step_by_step = args.step_by_step
    Game.manual = args.manual

    # Print the arguments (for debugging purposes)
    print(f'Sessions: {Game.sessions}')
    print(f'Boardsize: {Game.boardsize}')
    print(f'Save Path: {Game.save_path}')
    print(f'Load Path: {Game.load_path}')
    print(f'Visual: {Game.visual}')
    print(f'Dontlearn: {Game.dontlearn}')
    print(f'Step-by-Step: {Game.step_by_step}')

    # Add your training logic here
    random.seed(42)
    if Game.manual:
        play = Visualize()
        play.run()
    else:
        play = Interpreter()
        play.run()

if __name__ == '__main__':
    main()