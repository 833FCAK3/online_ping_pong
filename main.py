import pygame

from ball import Ball
from functions import check_events, update_positioning, update_screen
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
        check_events(paddle, stats, scoreboard, restart_button, ball)
        update_positioning(paddle, ball, stats, scoreboard, settings)
        update_screen(screen, settings, paddle, stats, scoreboard, restart_button, ball, game_over_msg)

        # Limit fps
        if lock_fps:
            clock.tick(settings.fps)


if __name__ == "__main__":
    run_game(lock_fps=True)
