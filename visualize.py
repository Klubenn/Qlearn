import random
import time
import pygame
from environment import Environment
from utils import Stats, Step, GameState, Movement, CELL, KeyEvent, Settings


class Visualize:
    def __init__(self) -> None:
        pygame.init()
        self.window_width = Settings.env_size * CELL
        self.window_height = Settings.env_size * CELL
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Learn2Slither")

    def draw_state(self, state):
        self.window.fill((25, 25, 25))
        def draw_rect(x, y, color):
            pygame.draw.rect(self.window, color, (x * CELL, y * CELL, CELL, CELL))

        def draw_circle(x, y, color):
            pygame.draw.circle(self.window, color, (x * CELL + CELL / 2, y * CELL + CELL / 2), 20)

        def draw_board():
            for i in range(Settings.boardsize + 1):
                iterate = CELL * i + CELL
                pygame.draw.line(self.window, "white", (CELL, iterate), (CELL * Settings.boardsize + CELL, iterate), 2)
                pygame.draw.line(self.window, "white", (iterate, CELL), (iterate, CELL * Settings.boardsize + CELL), 2)

        for i, array in enumerate(state):
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
        pygame.display.update()

    def catch_key_event(self) -> KeyEvent|None:
        """
        Catch key events and return the corresponding key event.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return KeyEvent.EXIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return KeyEvent.CONTINUE

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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    env.move(Movement.move_right(env.snake_position[0]))
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    env.move(Movement.move_left(env.snake_position[0]))
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    env.move(Movement.move_up(env.snake_position[0]))
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    env.move(Movement.move_down(env.snake_position[0]))
            
            if Step.state != GameState.RUNNING:
                self.window.fill((25, 25, 25))
                self.draw_state(env.state)
                font = pygame.font.Font('Decay-M5RB.ttf', 50)
                phrase = 'You won!' if Step.state == GameState.WON else 'Game Over!'
                text = font.render(phrase, False, (255, 0, 0))
                self.window.blit(text, (100, 250))
                pygame.display.update()
                time.sleep(1)
                Stats.round += 1
                Step.state = GameState.RUNNING
                print("Game over")
                print(f"Snake length: {len(env.snake_position)}")
                print(f"Rounds played: {Stats.round}")
                env = Environment()

            self.draw_state(env.state)

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    random.seed(42)
    play = Visualize()
    play.run()

