import time

import pygame

from game_stats import GameStats
from multiplayer.ball import Ball
from multiplayer.functions import check_events, check_exit, update_positioning, update_screen
from multiplayer.menu import Arrow, BaseText, Button, GameJoever, Strikes
from multiplayer.network import Network
from multiplayer.paddle import Paddle
from multiplayer.scoreboard import Scoreboard
from settings import Settings


def multiplayer(settings: Settings, screen: pygame.Surface) -> None:
    # Network
    net = Network(settings)

    net.send(settings.max_rez)

    waiting_msg = BaseText(screen, 50, "Waiting for the other player to connect")
    waiting_msg.render()
    pygame.display.flip()

    # Retrieve negotiated resolution
    resolution = None
    while not resolution:
        check_exit()
        resolution = net.send("rez")
        time.sleep(1 / 30)

    # Initialize screen, game settings, statistics, scoreboard, fps limiter
    pygame.init()
    stats = GameStats(settings)
    display = pygame.display.get_desktop_sizes().index(resolution)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display)

    pygame.display.set_caption("Ping Pong Game")
    clock = pygame.time.Clock()

    # Game entities
    player_number = net.get_player_number()
    print(f"player_{player_number}")
    paddle_1 = Paddle(settings, player_number, 1)
    paddle_2 = Paddle(settings, player_number, 2)
    paddle_1.post_init(screen, net)
    paddle_2.post_init(screen, net)

    # Sends x coordinate of player's paddle to the server
    net.send(paddle_1.rect.x)
    print("Sent x coords to the server")

    # Menu items
    restart_button = Button(screen, stats, "Ready", "Ready")
    game_over_msg = GameJoever(screen)
    strikes_msg = Strikes(screen, stats)
    arrow = Arrow(screen, player_number)

    scoreboard = Scoreboard(screen, settings, stats, paddle_1, paddle_2)
    ball = Ball(screen, settings, net)

    run = [True]
    while run[0]:
        check_events(run, paddle_1, paddle_2, stats, scoreboard, settings, restart_button, ball, net)

        if stats.game_active:
            update_positioning(paddle_1, paddle_2, ball, stats, scoreboard, settings, net, game_over_msg, player_number)

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
            strikes_msg,
            arrow,
        )

        # Limit fps
        clock.tick(settings.fps)
