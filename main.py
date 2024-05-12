import pygame

from ball import Ball
from functions import check_events, update_positioning, update_screen
from game_stats import GameStats
from menu import Button, GameJoever, HighScore, Score
from paddle import Paddle
from scoreboard import Scoreboard
from settings import Settings


def run_game(lock_fps: bool):
    # Initialize screen, game settings, statistics, scoreboard, fps limiter
    pygame.init()
    settings = Settings()
    stats = GameStats(settings)
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height), display=0)
    pygame.display.set_caption("Ping Pong Game")
    scoreboard = Scoreboard(screen, settings, stats)
    clock = pygame.time.Clock()

    # Menu items
    restart_button = Button(screen, stats, "Restart", "Start")
    game_over_msg = GameJoever(screen)
    score_msg = Score(screen, stats)
    high_score_msg = HighScore(screen, stats)

    # Game entities
    paddle = Paddle(screen, settings)
    ball = Ball(screen, settings)

    while True:
        check_events(paddle, stats, scoreboard, restart_button, ball, score_msg)
        if stats.game_active:
            update_positioning(paddle, ball, stats, scoreboard, settings, score_msg, high_score_msg)
        update_screen(
            screen, settings, paddle, stats, scoreboard, restart_button, ball, game_over_msg, score_msg, high_score_msg
        )

        # Limit fps
        if lock_fps:
            clock.tick(settings.fps)


if __name__ == "__main__":
    run_game(lock_fps=True)
