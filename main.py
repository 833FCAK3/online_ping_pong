import sys

import pygame

from ball import Ball
from functions import check_collision
from game_stats import GameStats
from paddle import Paddle


def run_game():
    pygame.init()
    bg_colour = (200, 200, 200)
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("Ping Pong Game")
    stats = GameStats()

    paddle = Paddle(screen)
    ball = Ball(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_a:
                        paddle.moving_left = True
                    case pygame.K_d:
                        paddle.moving_right = True
            elif event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_a:
                        paddle.moving_left = False
                    case pygame.K_d:
                        paddle.moving_right = False

        if stats.game_active:
            screen.fill(bg_colour)
            paddle.update_position()
            paddle.render()
            ball.update_position_env()
            ball.render()
            check_collision(paddle, ball, stats)

        pygame.display.flip()


run_game()
