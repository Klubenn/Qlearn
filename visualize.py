import random
import time
import pygame
from environment import Environment
from utils import (
    Stats,
    Step,
    GameState,
    Movement,
    KeyEvent,
    Settings,
    CELL,
    BOARD_SIZE,
)


class Visualize:
    def __init__(self) -> None:
        pygame.init()
        self.playfield = max(Settings.env_size, BOARD_SIZE + 2)
        self.window_width = self.playfield * CELL + 400
        self.window_height = self.playfield * CELL
        self.window = pygame.display.set_mode((self.window_width,
                                               self.window_height))
        pygame.display.set_caption("Learn2Slither")

    def draw_state(self, env: Environment, exploitation_rate=None) -> None:
        self.window.fill((25, 25, 25))

        def draw_rect(x, y, color):
            pygame.draw.rect(self.window, color, (x * CELL, y * CELL,
                                                  CELL, CELL))

        def draw_circle(x, y, color):
            pygame.draw.circle(self.window, color, (x * CELL + CELL / 2,
                                                    y * CELL + CELL / 2), 20)

        def draw_board():
            for i in range(Settings.boardsize + 1):
                iterate = CELL * i + CELL
                pygame.draw.line(self.window,
                                 "white",
                                 (CELL, iterate),
                                 (CELL * Settings.boardsize + CELL, iterate),
                                 2)
                pygame.draw.line(self.window,
                                 "white",
                                 (iterate, CELL),
                                 (iterate, CELL * Settings.boardsize + CELL),
                                 2)

        def draw_stats():
            font = pygame.font.SysFont('freesans', 25)
            info = [f'Rounds: {Stats.round}',
                    f'Current length: {len(env.snake_position)}',
                    f'Maximum length: {max(Stats.all_lengths)}'
                    if Stats.all_lengths else '',
                    f'Exploitation rate: {exploitation_rate:.2f}'
                    if exploitation_rate is not None else '',
                    f'Current speed: {1 / Settings.delay:.1f} cells/s'
                    if not Settings.step_by_step and not Settings.manual
                    else '',
                    'Press SPACE to continue' if Settings.step_by_step
                    else '',
                    ]
            for i in range(len(info)):
                text = font.render(info[i], False, (255, 255, 255))
                self.window.blit(text, (self.playfield * CELL + 20,
                                        i * 50 + 20))

        for i, array in enumerate(env.state):
            for j, value in enumerate(array):
                if value == 'W':
                    draw_rect(j, i, "grey")
                elif value == 'H':
                    draw_rect(j, i, (35, 35, 150))
                elif value == 'S':
                    draw_rect(j, i, (35, 100, 255))
                elif value == 'G':
                    draw_circle(j, i, "green")
                elif value == 'R':
                    draw_circle(j, i, "red")
                elif value == '0':
                    pass
        draw_board()
        draw_stats()
        pygame.display.update()

    def catch_key_event(self) -> KeyEvent | None:
        """
        Catch key events and return the corresponding key event.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                             and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return KeyEvent.EXIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return KeyEvent.CONTINUE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                return KeyEvent.UP
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                return KeyEvent.DOWN

    def run(self):
        """
        Runs the game loop, handling events and updating the game state.
        """
        env = Environment()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif (event.type == pygame.KEYDOWN
                      and event.key == pygame.K_ESCAPE):
                    running = False
                elif (event.type == pygame.KEYDOWN
                      and event.key == pygame.K_RIGHT):
                    env.move(Movement.move_right(env.snake_position[0]))
                elif (event.type == pygame.KEYDOWN
                      and event.key == pygame.K_LEFT):
                    env.move(Movement.move_left(env.snake_position[0]))
                elif (event.type == pygame.KEYDOWN
                      and event.key == pygame.K_UP):
                    env.move(Movement.move_up(env.snake_position[0]))
                elif (event.type == pygame.KEYDOWN
                      and event.key == pygame.K_DOWN):
                    env.move(Movement.move_down(env.snake_position[0]))

            if Step.state != GameState.RUNNING:
                self.window.fill((25, 25, 25))
                self.draw_state(env)
                font = pygame.font.Font('Decay-M5RB.ttf', 50)
                phrase = ('You won!' if Step.state == GameState.WON
                          else 'Game Over!')
                text = font.render(phrase, False, (255, 0, 0))
                self.window.blit(text, (100, 250))
                pygame.display.update()
                time.sleep(1)
                Stats.round += 1
                Stats.all_lengths.append(len(env.snake_position))
                Step.state = GameState.RUNNING
                env = Environment()

            self.draw_state(env)

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    random.seed(42)
    play = Visualize()
    play.run()
