import argparse
import random
import statistics
from interpreter import Interpreter
from utils import LIMIT_DURATION, Game, Stats
from visualize import Visualize

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Train a snake game AI model.")
    parser.add_argument('--sessions', type=int, default=10, help='The number of training sessions to perform')
    parser.add_argument('--boardsize', type=int, default=10, help='The size of the board')
    parser.add_argument('--save', type=str, help='The path where the result of the training will be saved')
    parser.add_argument('--load', type=str, help='The path where the training will be loaded from')
    parser.add_argument('--visual', action='store_true', help='Display training progress')
    parser.add_argument('--exploit', action='store_true', help="If present, the model doesn't explore")
    parser.add_argument('--dontlearn', action='store_true', help="If present, the model won't update q-table")
    parser.add_argument('--step-by-step', action='store_true', help='If present, the model will wait for user input after each move')
    parser.add_argument('--manual', action='store_true', help='Play the game manually')
    parser.add_argument('--fill-zeroes', action='store_true', help='Priorities filling zero values in the q-table')
    
    args = parser.parse_args()

    Game.sessions = args.sessions
    Game.boardsize = args.boardsize
    Game.env_size = args.boardsize + 2
    Game.save_path = args.save
    Game.load_path = args.load
    Game.step_by_step = args.step_by_step
    Game.visual = args.visual or args.step_by_step
    Game.dontlearn = args.dontlearn
    Game.exploit = args.exploit or args.dontlearn
    Game.manual = args.manual
    Game.fill_zeroes = args.fill_zeroes
    

def print_stats():
    """
    Print the statistics of the training.
    """
    print()
    # print('Statistics:')
    if Game.load_path:
        print(f'Filename = {Game.load_path}')
    print(f'Number of sessions = {Game.sessions}')
    print(f'Limit duration = {LIMIT_DURATION}')
    try:
        print(f'max length = {max(Stats.max_length)}')
        print(f'median length = {int(statistics.median(Stats.all_lengths))}')
        print(f'mean length = {int(statistics.mean(Stats.all_lengths))}')
    except Exception as e:
        print(f'Error calculating stats: {e}')
    print(f'% breaks = {(Stats.breaks / Game.sessions * 100):.4}')
    print(f'% not ten = {(Stats.not_ten / Game.sessions * 100):.2f}')


def main():
    parse_arguments()
    random.seed(8)
    try:
        if Game.manual:
            play = Visualize()
            play.run()
        else:
            play = Interpreter()
            play.run()
            if Game.save_path:
                play.ag.save_q_table(Game.save_path)
    except KeyboardInterrupt:
        pass
    
    print_stats()
    

if __name__ == '__main__':
    main()
