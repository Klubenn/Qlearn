import argparse
import random
import statistics

from matplotlib import pyplot as plt
import yaml
from interpreter import Interpreter
from utils import Settings, Stats
from visualize import Visualize

import pandas as pd


def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Train a snake game AI model.")
    parser.add_argument('--config', type=str, help='Path to the configuration \
                        file. If present, the configuration file will be used \
                        instead of command-line arguments.')
    parser.add_argument('--sessions', type=int, default=10, help='The number \
                        of training sessions per epoch')
    parser.add_argument('--boardsize', type=int, default=10, help='The size \
                        of the board')
    parser.add_argument('--save', type=str, help='The postfix that will be \
                        added to the number of training sessions performed \
                        under which the model will be saved')
    parser.add_argument('--load', type=str, help='The path where the training \
                        will be loaded from')
    parser.add_argument('--visual', action='store_true', help='Display \
                        training progress graphically')
    parser.add_argument('--exploit', action='store_true', help="If present, \
                        the model doesn't explore")
    parser.add_argument('--dontlearn', action='store_true', help="If present, \
                        the model won't update q-table")
    parser.add_argument('--step-by-step', action='store_true', help='If \
                        present, the model will wait for user input after \
                        each move')
    parser.add_argument('--manual', action='store_true', help='Play the \
                        Settings.manually')
    parser.add_argument('--universal', action='store_true', help='Train the \
                        model that would work on any board size')
    parser.add_argument('--seed', type=int,
                        default=random.randint(0, 2**32 - 1),
                        help='Seed for random number generator')
    parser.add_argument('--epochs', type=int, default=1, help='Number of \
                        epochs to train the model')
    return parser.parse_args()


def apply_cl_settings(args):
    Settings.sessions = args.sessions
    Settings.boardsize = args.boardsize
    Settings.env_size = args.boardsize + 2
    Settings.save_path = args.save
    Settings.load_path = args.load
    Settings.step_by_step = args.step_by_step
    Settings.visual = args.visual or args.step_by_step
    Settings.dontlearn = args.dontlearn
    Settings.exploit = args.exploit or args.dontlearn
    Settings.manual = args.manual
    Settings.universal = args.universal
    Settings.seed = args.seed
    Settings.epochs = args.epochs


def apply_config_settings(settings):
    Settings.sessions = settings.get('sessions', 10)
    Settings.boardsize = settings.get('boardsize', 10)
    Settings.env_size = Settings.boardsize + 2
    Settings.save_path = settings.get('save')
    Settings.load_path = settings.get('load')
    Settings.step_by_step = settings.get('step-by-step', False)
    Settings.visual = settings.get('visual', False) or settings.get(
        'step-by-step', False)
    Settings.dontlearn = settings.get('dontlearn', False)
    Settings.exploit = settings.get('exploit', False) or settings.get(
        'dontlearn', False)
    Settings.manual = settings.get('manual', False)
    Settings.universal = settings.get('universal', False)
    Settings.seed = settings.get('seed', random.randint(0, 2**32 - 1))
    Settings.epochs = settings.get('epochs', 1)


def load_config(config_path):
    print(config_path)
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


def print_stats(stat_dict: dict) -> None:
    """
    Print the statistics.
    """
    df = pd.DataFrame(stat_dict)
    print(df)
    plot_stats(df)


def plot_stats(df: pd.DataFrame) -> None:
    """
    Plot the statistics.
    """
    _, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    if any(df['model_name']):
        x_value = df['model_name']
        x_name = 'Model Name'
    else:
        x_value = df['epoch']
        x_name = 'Epoch'
    ax1.plot(x_value, df['max_length'], marker='o',
             label='Max Length')
    ax1.plot(x_value, df['mean_length'], marker='o',
             label='Mean Length')
    ax2.plot(x_value, df['%_not_ten'], marker='x',
             linestyle='--', color='g', label='% Below Ten')

    ax1.set_title('Model Statistics')
    ax1.set_xlabel(x_name)
    ax1.set_ylabel('Length Values')
    ax1.set_xticks(range(len(x_value)))  # Ensure proper alignment
    ax1.set_xticklabels(x_value, rotation=45, ha='right')  # Use actual x_value for labels
    ax2.set_ylabel('Percentage Values')

    ax1.set_ylim(0, max(df['max_length']) + 10)
    ax2.set_ylim(0, 100)

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()


def update_stat_dict(stat_dict: dict, epoch=0, model_name='') -> None:
    stat_dict['model_name'].append(model_name.split('/')[-1])
    stat_dict['epoch'].append(epoch)
    stat_dict['max_length'].append(max(Stats.max_length))
    stat_dict['median_length'].append(int(statistics.median(
        Stats.all_lengths)))
    stat_dict['mean_length'].append(int(statistics.mean(Stats.all_lengths)))
    stat_dict['%_breaks'].append(Stats.breaks / Settings.sessions * 100)
    stat_dict['%_not_ten'].append(Stats.not_ten / Settings.sessions * 100)


def train_model(stat_dict: dict):
    """
    Train the model.
    """
    play = Interpreter()
    for i in range(Settings.epochs):
        play.run()
        if Settings.save_path:
            try:
                number, exp = 0, 0
                if Settings.load_path:
                    number = Settings.load_path.split('/')[-1].split('_')[0]
                    separate = number.split('k')
                    number = int(separate[0]) * 1000 ** (len(separate) - 1)
                number += (i + 1) * Settings.sessions
                exp = 0
                while number % 1000 == 0:
                    exp += 1
                    number //= 1000
                save_name = f'{number}{"k" * exp}_' + Settings.save_path
            except Exception:
                print('Unseccessful parsing of the model name, saving with \
                      default name')
                save_name = Settings.save_path
            play.ag.save_q_table(save_name)
            update_stat_dict(stat_dict, epoch=i, model_name=save_name)
        else:
            update_stat_dict(stat_dict, epoch=i)
        Stats.reset_stats()

    print_stats(stat_dict)


def evaluate_model(stat_dict: dict):
    """
    Evaluate the model.
    """
    if type(Settings.load_path) is not list:
        Settings.load_path = [Settings.load_path]
    load_paths = Settings.load_path
    for path in load_paths:
        random.seed(Settings.seed)
        Settings.load_path = path
        play = Interpreter()
        play.run()
        if Settings.save_path:
            play.ag.save_q_table(Settings.save_path)
        update_stat_dict(stat_dict, model_name=path)
        Stats.reset_stats()
    print_stats(stat_dict)


def main():
    args = parse_arguments()
    if args.config:
        settings = load_config(args.config)
        apply_config_settings(settings)
    else:
        apply_cl_settings(args)
    random.seed(Settings.seed)
    stat_dict = {
        'model_name': [],
        'epoch': [],
        'max_length': [],
        'median_length': [],
        'mean_length': [],
        '%_breaks': [],
        '%_not_ten': []
    }
    try:
        if Settings.manual:
            play = Visualize()
            play.run()
        else:
            if Settings.save_path or not Settings.load_path:
                train_model(stat_dict)
            elif Settings.load_path:
                evaluate_model(stat_dict)
    except KeyboardInterrupt:
        print()


if __name__ == '__main__':
    main()
