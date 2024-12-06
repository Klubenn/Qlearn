import random
import time
import pygame
from environment import Environment
from utils import Game, Movement
# from pygame.locals import *

CELL = 50
BOARD_SIZE = 10

def tutorial():
    pygame.init()

    window_width = 800
    window_height = 600
    window = pygame.display.set_mode((window_width, window_height))

    player_x = 32
    player_y = 32
    clock = pygame.time.Clock()

    running = True
    while running:
        delta_time = clock.tick(60) / 1000 # set the frame rate and link the movement to real time pro sec
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #     player_x += 32

        keys = pygame.key.get_pressed()
        speed = 240
        if keys[pygame.K_RIGHT]:
            player_x += speed * delta_time
        elif keys[pygame.K_LEFT]:
            player_x -= speed * delta_time
        elif keys[pygame.K_DOWN]:
            player_y += speed * delta_time
        elif keys[pygame.K_UP]:
            player_y -= speed * delta_time
        

        window.fill((25, 25, 25))
        
        # draw rectangle
        x, y = 32, 32
        width = 100
        height = 200
        pygame.draw.rect(window, "red", (x, y, width, height))

        # draw circle
        pygame.draw.circle(window, (35, 100, 200), (window_width / 2, window_height / 2), 20)

        # draw line
        pygame.draw.line(window, "white", (20, 20), (window_width - 20, 20), 5)

        pygame.draw.rect(window, "red", (player_x, player_y, 64, 64))

        pygame.display.update()

    pygame.quit()

class Visualize:
    def __init__(self) -> None:
        pygame.init()
        self.window_width = 600
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Learn2Slither")
        self.run()


    def draw_state(self, state):

        def draw_rect(x, y, color):
            pygame.draw.rect(self.window, color, (x * CELL, y * CELL, CELL, CELL))

        def draw_circle(x, y, color):
            pygame.draw.circle(self.window, color, (x * CELL + CELL / 2, y * CELL + CELL / 2), 20)

        def draw_board():
            for i in range(BOARD_SIZE + 1):
                iterate = CELL * i + CELL
                pygame.draw.line(self.window, "white", (CELL, iterate), (CELL * BOARD_SIZE + CELL, iterate), 2)
                pygame.draw.line(self.window, "white", (iterate, CELL), (iterate, CELL * BOARD_SIZE + CELL), 2)

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

    def run(self):
        env = Environment(BOARD_SIZE)
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
            
            if Game.game_over == 1:
                self.window.fill((25, 25, 25))
                self.draw_state(env.state)
                font = pygame.font.Font('Decay-M5RB.ttf', 50)
                text = font.render('Game Over!', False, (255, 0, 0))
                self.window.blit(text, (100, 250))
                pygame.display.update()
                time.sleep(2)
                Game.round += 1
                Game.game_over = 0
                print("Game over")
                print(f"Snake length: {len(env.snake_position)}")
                print(f"Rounds played: {Game.round}")
                env = Environment(BOARD_SIZE)


            self.window.fill((25, 25, 25))
            self.draw_state(env.state)

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    random.seed(42)
    Visualize()
