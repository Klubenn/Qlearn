import argparse
import random
from interpreter import Interpreter
from utils import Game, Stats
from visualize import Visualize
from statistics import mean 

def parse_arguments():
    parser = argparse.ArgumentParser(description="Train a snake game AI model.")
    parser.add_argument('--sessions', type=int, default=10, help='The number of training sessions to perform')
    parser.add_argument('--boardsize', type=int, default=10, help='The size of the board')
    parser.add_argument('--save', type=str, help='The path where the result of the training will be saved')
    parser.add_argument('--load', type=str, help='The path where the training will be loaded from')
    parser.add_argument('--visual', action='store_true', help='Display training progress')
    parser.add_argument('--exploit', action='store_true', help="If present, the model doesn't explore")
    parser.add_argument('--dontlearn', action='store_true', help="If present, the model won't update q-table")
    parser.add_argument('--randchoice', action='store_true', help="If present, the agent will select random maximum direction from the q-table")
    parser.add_argument('--step-by-step', action='store_true', help='If present, the model will wait for user input after each move')
    parser.add_argument('--manual', action='store_true', help='Play the game manually')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    Game.sessions = args.sessions
    Game.boardsize = args.boardsize
    Game.env_size = args.boardsize + 2
    Game.save_path = args.save
    Game.load_path = args.load
    Game.visual = args.visual
    Game.exploit = args.dontlearn or args.exploit
    Game.dontlearn = args.dontlearn
    Game.randchoice = args.randchoice
    Game.step_by_step = args.step_by_step
    Game.manual = args.manual

    random.seed(42)
    if Game.manual:
        play = Visualize()
        play.run()
    else:
        play = Interpreter()
        play.run()
    print(f"Game over, avg max length = {float(mean(Stats.max_length)):.2f}, avg length = {float(mean(Stats.all_lengths)):.2f}, \
% breaks = {(Stats.breaks / Game.sessions * 100):.4}, % not ten = {(Stats.not_ten / Game.sessions * 100):.4f}")
    

if __name__ == '__main__':
    main()