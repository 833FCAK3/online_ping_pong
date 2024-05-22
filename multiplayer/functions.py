import sys
import time

import pygame

from game_stats import GameStats
from multiplayer.ball import Ball
from multiplayer.menu import Arrow, Button, GameJoever, Strikes
from multiplayer.network import Network
from multiplayer.paddle import Paddle
from multiplayer.scoreboard import Scoreboard
from settings import Settings


def check_ball_collision(
    paddle_1: Paddle,
    paddle_2: Paddle,
    ball: Ball,
    stats: GameStats,
    scoreboard: Scoreboard,
    settings: Settings,
    net: Network,
    game_over_msg: GameJoever,
    player_number: int,
) -> None:
    """Changes ball's direction and speed on collision with the paddle, left, right, top and bottom of the screen,
    reduces life count in the latter case"""
    paddles = [paddle_1.rect, paddle_2.rect] if player_number == 1 else [paddle_2.rect, paddle_1.rect]
    collision = ball.rect.collidelist(paddles)

    if collision == 0:
        if not ball.lock_1:
            ball.lock_1 = True
            ball.moving_down, ball.moving_up = not ball.moving_down, not ball.moving_up
            ball.speed *= settings.speed_up_factor
            stats.strikes += 1
    elif collision == 1:
        if not ball.lock_2:
            ball.lock_2 = True
            ball.moving_down, ball.moving_up = not ball.moving_down, not ball.moving_up
            ball.speed *= settings.speed_up_factor
            stats.strikes += 1
    elif ball.rect.bottom >= ball.screen_rect.bottom:
        minus_life(stats, scoreboard, net, game_over_msg, player_number, 1)
    elif ball.rect.top <= ball.screen_rect.top:
        minus_life(stats, scoreboard, net, game_over_msg, 2 // player_number, 2)

    # Change direction on collision with left, right, top or bottom side of the screen
    if ball.rect.left == ball.screen_rect.left:
        ball.moving_left, ball.moving_right = False, True
    if ball.rect.right == ball.screen_rect.right:
        ball.moving_left, ball.moving_right = True, False
    if ball.rect.bottom >= ball.screen_rect.bottom:
        ball.moving_down, ball.moving_up = not ball.moving_down, not ball.moving_up
        ball.lock_1 = True
    if ball.rect.top <= ball.screen_rect.top:
        ball.moving_down, ball.moving_up = not ball.moving_down, not ball.moving_up
        ball.lock_2 = True

    if ball.rect.y > ball.screen_rect.centery:
        ball.lock_2 = False
    elif ball.rect.y < ball.screen_rect.centery:
        ball.lock_1 = False


def minus_life(
    stats: GameStats,
    scoreboard: Scoreboard,
    net: Network,
    game_over_msg: GameJoever,
    paddle_number: int,
    height_number: int,
):
    lives_left_str = f"lives_left_{paddle_number}"
    lives_left = getattr(stats, lives_left_str) - 1

    setattr(stats, lives_left_str, lives_left)

    scoreboard.prep_lives()
    if lives_left == 0:
        game_over_msg.msg = f"PLAYER {int(2 / height_number)} WINS!"
        stats.game_active = False
        net.send("game over")
        pygame.mouse.set_visible(True)
        return


def check_restart_button(
    stats: GameStats,
    scoreboard: Scoreboard,
    settings: Settings,
    restart_button: Button,
    paddle_1: Paddle,
    paddle_2: Paddle,
    ball: Ball,
    net: Network,
    mouse_x,
    mouse_y,
) -> None:
    """Starts and restarts the game"""
    button_clicked = restart_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        restart_game(stats, scoreboard, settings, paddle_1, paddle_2, ball, net)


def restart_game(
    stats: GameStats,
    scoreboard: Scoreboard,
    settings: Settings,
    paddle_1: Paddle,
    paddle_2: Paddle,
    ball: Ball,
    net: Network,
) -> None:
    """Performs a ready check, starts and restarts the game"""
    net.send("rdy")

    while True:
        check_exit()
        opponent_rdy = net.send("rdy_check")
        if opponent_rdy == True:
            break
        time.sleep(1 / settings.fps)

    if not stats.game_started:
        stats.game_started = True

    if not stats.game_active:
        pygame.mouse.set_visible(False)
        paddle_1.center_paddle()
        paddle_2.center_paddle()
        ball.respawn_ball()

        # Reset game stats
        stats.game_active = True
        stats.reset_stats()
        scoreboard.prep_lives()


def check_events(
    paddle_1: Paddle,
    paddle_2: Paddle,
    stats: GameStats,
    scoreboard: Scoreboard,
    settings: Settings,
    restart_button: Button,
    ball: Ball,
    net: Network,
) -> None:
    """Responds to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_a | pygame.K_LEFT:
                    paddle_1.moving_left = True
                case pygame.K_d | pygame.K_RIGHT:
                    paddle_1.moving_right = True
                case pygame.K_SPACE:
                    restart_game(stats, scoreboard, settings, paddle_1, paddle_2, ball, net)
                case pygame.K_q:
                    sys.exit()
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_a | pygame.K_LEFT:
                    paddle_1.moving_left = False
                case pygame.K_d | pygame.K_RIGHT:
                    paddle_1.moving_right = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_restart_button(
                stats, scoreboard, settings, restart_button, paddle_1, paddle_2, ball, net, mouse_x, mouse_y
            )


def check_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_q:
                    sys.exit()


def update_positioning(
    paddle_1: Paddle,
    paddle_2: Paddle,
    ball: Ball,
    stats: GameStats,
    scoreboard: Scoreboard,
    settings: Settings,
    net: Network,
    game_over_msg: GameJoever,
    player_number: int,
) -> None:
    """Updates positioning of the game objects"""
    scoreboard.reposition_lives()
    paddle_2_x = paddle_1.update_position()
    paddle_2.update_position(paddle_2_x)
    ball.update_position()

    check_ball_collision(paddle_1, paddle_2, ball, stats, scoreboard, settings, net, game_over_msg, player_number)


def update_screen(
    screen: pygame.Surface,
    settings: Settings,
    paddle_1: Paddle,
    paddle_2: Paddle,
    stats: GameStats,
    scoreboard: Scoreboard,
    restart_button: Button,
    ball: Ball,
    game_over_msg: GameJoever,
    strikes_msg: Strikes,
    arrow: Arrow,
) -> None:
    """Updates images on the screen, and flips to the new screen."""
    if not stats.game_started:
        arrow.render()

    if stats.game_started:
        screen.fill(settings.bg_colour)
        paddle_1.render()
        paddle_2.render()
        scoreboard.lives_1.draw(screen)
        scoreboard.lives_2.draw(screen)
        ball.render()

    if not stats.game_active:
        restart_button.render()
        if stats.game_started:
            game_over_msg.render()
            strikes_msg.render()

    pygame.display.flip()
