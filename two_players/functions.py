import sys

import pygame

from game_stats import GameStats
from settings import Settings
from two_players.ball import Ball
from two_players.menu import Button, GameJoever, Strikes
from two_players.paddle import Paddle
from two_players.scoreboard import Scoreboard


def check_ball_collision(
    paddle_1: Paddle,
    paddle_2: Paddle,
    ball: Ball,
    stats: GameStats,
    scoreboard: Scoreboard,
    settings: Settings,
    game_over_msg: GameJoever,
) -> None:
    """Changes ball's direction and speed on collision with the paddle, left, right, top and bottom of the screen,
    reduces life count in the latter case"""
    collision = ball.rect.collidelist([paddle_1.rect, paddle_2.rect])

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
        minus_life(stats, scoreboard, game_over_msg, 1)
    elif ball.rect.top <= ball.screen_rect.top:
        minus_life(stats, scoreboard, game_over_msg, 2)

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


def minus_life(stats: GameStats, scoreboard: Scoreboard, game_over_msg: GameJoever, player_number: int) -> None:
    lives_left_str = f"lives_left_{player_number}"
    lives_left = getattr(stats, lives_left_str) - 1

    setattr(stats, lives_left_str, lives_left)

    scoreboard.prep_lives()
    if lives_left == 0:
        game_over_msg.msg = f"PLAYER {int(2 / player_number)} WINS!"
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_restart_button(
    stats: GameStats,
    scoreboard: Scoreboard,
    restart_button: Button,
    paddle_1: Paddle,
    paddle_2: Paddle,
    ball: Ball,
    mouse_x,
    mouse_y,
) -> None:
    """Starts and restarts the game"""
    button_clicked = restart_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        restart_game(stats, scoreboard, paddle_1, paddle_2, ball)


def restart_game(stats: GameStats, scoreboard: Scoreboard, paddle_1: Paddle, paddle_2: Paddle, ball: Ball) -> None:
    """Starts and restarts the game"""
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
    run: list[bool],
    paddle_1: Paddle,
    paddle_2: Paddle,
    stats: GameStats,
    scoreboard: Scoreboard,
    restart_button: Button,
    ball: Ball,
) -> None:
    """Responds to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_a:
                    paddle_1.moving_left = True
                case pygame.K_d:
                    paddle_1.moving_right = True
                case pygame.K_LEFT:
                    paddle_2.moving_left = True
                case pygame.K_RIGHT:
                    paddle_2.moving_right = True
                case pygame.K_SPACE:
                    restart_game(stats, scoreboard, paddle_1, paddle_2, ball)
                case pygame.K_q:
                    run[0] = False
                    pygame.mouse.set_visible(True)
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_a:
                    paddle_1.moving_left = False
                case pygame.K_d:
                    paddle_1.moving_right = False
                case pygame.K_LEFT:
                    paddle_2.moving_left = False
                case pygame.K_RIGHT:
                    paddle_2.moving_right = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_restart_button(stats, scoreboard, restart_button, paddle_1, paddle_2, ball, mouse_x, mouse_y)


def update_positioning(
    paddle_1: Paddle,
    paddle_2: Paddle,
    ball: Ball,
    stats: GameStats,
    scoreboard: Scoreboard,
    settings: Settings,
    game_over_msg: GameJoever,
) -> None:
    """Updates positioning of the game objects"""
    scoreboard.reposition_lives()
    paddle_1.update_position()
    paddle_2.update_position()
    ball.update_position()

    check_ball_collision(paddle_1, paddle_2, ball, stats, scoreboard, settings, game_over_msg)


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
) -> None:
    """Updates images on the screen, and flips to the new screen."""
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
