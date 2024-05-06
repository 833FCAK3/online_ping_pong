import pygame

from ball import Ball
from game_stats import GameStats
from paddle import Paddle


def check_collision(paddle: Paddle, ball: Ball, stats: GameStats):
    if ball.rect.colliderect(paddle.rect):
        ball.moving_down, ball.moving_up = False, True
    if ball.rect.bottom == ball.screen_rect.bottom:
        print("Potracheno")
        stats.game_active = False
