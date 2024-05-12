import sys

import pygame

from ball import Ball
from game_stats import GameStats
from menu import Button, GameJoever, HighScore, Score
from paddle import Paddle
from scoreboard import Scoreboard
from settings import Settings


def check_ball_collision(
    paddle: Paddle,
    ball: Ball,
    stats: GameStats,
    scoreboard: Scoreboard,
    settings: Settings,
    score_msg: Score,
    high_score_msg: HighScore,
) -> None:
    """Changes ball's direction and speed on collision with the paddle, left, right, top and bottom of the screen, reduces life count in the latter case.
    Utilizes 'vulnerable' flag to not take away multiple lives in sigle bottom touch"""
    if ball.rect.colliderect(paddle.rect):
        if not stats.direction_speed_change_lock:
            stats.direction_speed_change_lock = True
            ball.moving_down, ball.moving_up = False, True
            ball.speed *= settings.speed_up_factor
            scoreboard.score()
            score_msg.reposition()
        if ball.rect.bottom >= ball.screen_rect.bottom:
            stats.vulnerable = True
    elif ball.rect.bottom >= ball.screen_rect.bottom and stats.vulnerable:
        stats.lives_left -= 1
        scoreboard.prep_lives()
        stats.vulnerable = False
        if stats.lives_left == 0:
            if stats.score > stats.high_score:
                stats.high_score = stats.score
                high_score_msg.reposition()
            stats.game_active = False
            pygame.mouse.set_visible(True)
            return

    # Change direction on collision with left, top or right side of the screen
    if ball.rect.left == ball.screen_rect.left:
        ball.moving_left, ball.moving_right = False, True
        stats.direction_speed_change_lock = False
    if ball.rect.right == ball.screen_rect.right:
        ball.moving_left, ball.moving_right = True, False
        stats.direction_speed_change_lock = False
    if ball.rect.top == ball.screen_rect.top:
        ball.moving_up, ball.moving_down = False, True
        stats.direction_speed_change_lock = False


def check_restart_button(
    stats: GameStats,
    scoreboard: Scoreboard,
    restart_button: Button,
    paddle: Paddle,
    ball: Ball,
    score_msg: Score,
    mouse_x,
    mouse_y,
) -> None:
    """Starts and restarts the game"""
    button_clicked = restart_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        restart_game(stats, scoreboard, paddle, ball, score_msg)


def restart_game(stats: GameStats, scoreboard: Scoreboard, paddle: Paddle, ball: Ball, score_msg: Score) -> None:
    """Starts and restarts the game"""
    if not stats.game_started:
        stats.game_started = True

    if not stats.game_active:
        pygame.mouse.set_visible(False)
        paddle.center_paddle()
        ball.respawn_ball()

        # Reset game stats
        stats.game_active = True
        stats.reset_stats()
        scoreboard.prep_lives()
        score_msg.reposition()


def check_events(
    paddle: Paddle, stats: GameStats, scoreboard: Scoreboard, restart_button: Button, ball: Ball, score_msg: Score
) -> None:
    """Responds to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_a:
                    paddle.moving_left = True
                case pygame.K_d:
                    paddle.moving_right = True
                case pygame.K_SPACE:
                    restart_game(stats, scoreboard, paddle, ball, score_msg)
                case pygame.K_q:
                    sys.exit()
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_a:
                    paddle.moving_left = False
                case pygame.K_d:
                    paddle.moving_right = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_restart_button(stats, scoreboard, restart_button, paddle, ball, score_msg, mouse_x, mouse_y)


def update_positioning(
    paddle: Paddle,
    ball: Ball,
    stats: GameStats,
    scoreboard: Scoreboard,
    settings: Settings,
    score_msg: Score,
    high_score_msg: HighScore,
) -> None:
    """Updates positioning of the game objects"""
    paddle.update_position()
    ball.update_position()

    check_ball_collision(paddle, ball, stats, scoreboard, settings, score_msg, high_score_msg)


def update_screen(
    screen: pygame.Surface,
    settings: Settings,
    paddle: Paddle,
    stats: GameStats,
    scoreboard: Scoreboard,
    restart_button: Button,
    ball: Ball,
    game_over_msg: GameJoever,
    score_msg: Score,
    high_score_msg: HighScore,
) -> None:
    """Updates images on the screen, and flips to the new screen."""
    if stats.game_started:
        screen.fill(settings.bg_colour)
        paddle.render()
        scoreboard.lives.draw(screen)
        score_msg.render()
        ball.render()

    if not stats.game_active:
        high_score_msg.render()
        restart_button.render()
        if stats.game_started:
            game_over_msg.render()

    pygame.display.flip()
