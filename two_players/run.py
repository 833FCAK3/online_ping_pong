import pygame

from two_players.ball import Ball
from two_players.functions import check_events, update_positioning, update_screen
from two_players.game_stats import GameStats
from two_players.menu import Button, GameJoever, HighScore, Score
from two_players.paddle import Paddle
from two_players.scoreboard import Scoreboard
from two_players.settings import Settings


def two_players():
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
    paddle_1 = Paddle(screen, settings, 1)
    paddle_2 = Paddle(screen, settings, 2)
    ball = Ball(screen, settings)

    while True:
        check_events(paddle_1, stats, scoreboard, restart_button, ball, score_msg)
        if stats.game_active:
            update_positioning(paddle_1, ball, stats, scoreboard, settings, score_msg, high_score_msg)
        update_screen(
            screen,
            settings,
            paddle_1,
            paddle_2,
            stats,
            scoreboard,
            restart_button,
            ball,
            game_over_msg,
            score_msg,
            high_score_msg,
        )

        # Limit fps
        clock.tick(settings.fps)
