import sys

import pygame

from ball import Ball
from functions import check_ball_collision, check_restart_button
from game_stats import GameStats
from menu import Button, Text
from paddle import Paddle
from scoreboard import Scoreboard
from settings import Settings


def run_game(lock_fps: bool):
    # Initialize screen, game settings, statistics, scoreboard, fps limiter
    pygame.init()
    settings = Settings()
    stats = GameStats(settings)
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Ping Pong Game")
    scoreboard = Scoreboard(screen, settings, stats)
    clock = pygame.time.Clock()

    # Menu items
    restart_button = Button(screen, stats, "Restart", "Start")
    game_over_msg = Text(screen, "GAME JOEVER!")

    # Game entities
    paddle = Paddle(screen, settings)
    ball = Ball(screen, settings)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_restart_button(stats, scoreboard, restart_button, paddle, ball, mouse_x, mouse_y)

        if stats.game_active:
            screen.fill(settings.bg_colour)
            paddle.update_position()
            paddle.render()
            ball.update_position_env()
            ball.render()
            check_ball_collision(paddle, ball, stats, scoreboard)
            scoreboard.lives.draw(screen)

        if not stats.game_active:
            restart_button.render()
            if stats.game_started:
                game_over_msg.render()

        pygame.display.flip()

        # Limit fps
        if lock_fps:
            clock.tick(settings.fps)


if __name__ == "__main__":
    run_game(lock_fps=True)
