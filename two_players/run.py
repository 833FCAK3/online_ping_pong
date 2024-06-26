import pygame

from game_stats import GameStats
from settings import Settings
from two_players.ball import Ball
from two_players.functions import check_events, update_positioning, update_screen
from two_players.menu import Button, GameJoever, Strikes
from two_players.paddle import Paddle
from two_players.scoreboard import Scoreboard


def two_players(settings: Settings) -> None:
    # Initialize screen, game settings, statistics, scoreboard, fps limiter
    pygame.init()
    stats = GameStats(settings)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=settings.display)
    pygame.display.set_caption("Ping Pong Game")
    clock = pygame.time.Clock()

    # Menu items
    restart_button = Button(screen, stats, "Restart", "Start")
    game_over_msg = GameJoever(screen)
    strikes_msg = Strikes(screen, stats)

    # Game entities
    paddle_1 = Paddle(screen, settings, 1)
    paddle_2 = Paddle(screen, settings, 2)
    scoreboard = Scoreboard(screen, settings, stats, paddle_1, paddle_2)
    ball = Ball(screen, settings)

    run = [True]
    while run[0]:
        check_events(run, paddle_1, paddle_2, stats, scoreboard, restart_button, ball)
        if stats.game_active:
            update_positioning(paddle_1, paddle_2, ball, stats, scoreboard, settings, game_over_msg)
        update_screen(
            screen, settings, paddle_1, paddle_2, stats, scoreboard, restart_button, ball, game_over_msg, strikes_msg
        )

        # Limit fps
        clock.tick(settings.fps)
