import pygame

from ball import Ball
from game_stats import GameStats
from menu import Button
from paddle import Paddle


def check_ball_collision(paddle: Paddle, ball: Ball, stats: GameStats):
    if ball.rect.colliderect(paddle.rect):
        ball.moving_down, ball.moving_up = False, True
    if ball.rect.bottom >= ball.screen_rect.bottom:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_restart_button(stats: GameStats, restart_button: Button, paddle: Paddle, ball: Ball, mouse_x, mouse_y):
    """Starts and restarts the game"""
    if not stats.game_started:
        stats.game_started = True

    button_clicked = restart_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        paddle.center_paddle()
        ball.respawn_ball()
        stats.game_active = True
