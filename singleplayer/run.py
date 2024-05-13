import pygame

from singleplayer.ball import Ball
from singleplayer.functions import check_events, update_positioning, update_screen
from singleplayer.game_stats import GameStats
from singleplayer.menu import Button, GameJoever, HighScore, Score
from singleplayer.paddle import Paddle
from singleplayer.scoreboard import Scoreboard
from singleplayer.settings import Settings


def single_player():
    # Initialize screen, game settings, statistics, scoreboard, fps limiter
    pygame.init()
    settings = Settings()
    stats = GameStats(settings)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=settings.display)
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
        clock.tick(settings.fps)
