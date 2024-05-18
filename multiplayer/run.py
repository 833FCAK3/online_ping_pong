import pygame

from multiplayer.ball import Ball
from multiplayer.functions import check_events, update_positioning, update_screen
from multiplayer.game_stats import GameStats
from multiplayer.menu import Button, GameJoever, Strikes
from multiplayer.network import Network
from multiplayer.paddle import Paddle
from multiplayer.scoreboard import Scoreboard
from multiplayer.settings import Settings


def multiplayer():
    # Initialize screen, game settings, statistics, scoreboard, fps limiter
    pygame.init()
    settings = Settings()
    stats = GameStats(settings)
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, display=0)
    screen = pygame.display.set_mode((950, 770), display=1)
    pygame.display.set_caption("Ping Pong Game")
    clock = pygame.time.Clock()

    # Menu items
    restart_button = Button(screen, stats, "Restart", "Start")
    game_over_msg = GameJoever(screen)
    strikes_msg = Strikes(screen, stats)

    # Network
    net = Network(settings)

    # Game entities
    player_number = net.get_player_number()
    print(f"player_{player_number}")  # TODO: display in a proper way on prep screen
    paddle_1 = Paddle(settings, player_number, 1)
    paddle_2 = Paddle(settings, player_number, 2)
    paddle_1.post_init(screen, net)
    paddle_2.post_init(screen, net)

    # Sends x coordinate of player's paddle to the server
    net.send(paddle_1.rect.x)
    print("Sent x coords to the server")

    scoreboard = Scoreboard(screen, settings, stats, paddle_1, paddle_2)
    ball = Ball(screen, settings)

    while True:
        check_events(paddle_1, paddle_2, stats, scoreboard, restart_button, ball)
        if stats.game_active:
            update_positioning(paddle_1, paddle_2, ball, stats, scoreboard, settings, game_over_msg)
        update_screen(
            screen, settings, paddle_1, paddle_2, stats, scoreboard, restart_button, ball, game_over_msg, strikes_msg
        )

        # Limit fps
        clock.tick(settings.fps)
