import pygame
from pygame.sprite import Group

from game_stats import GameStats
from multiplayer.life import Life
from multiplayer.paddle import Paddle
from multiplayer.settings import Settings


class Scoreboard:
    def __init__(
        self, screen: pygame.Surface, settings: Settings, stats: GameStats, paddle_1: Paddle, paddle_2: Paddle
    ) -> None:
        # Settings setup
        self.settings = settings
        self.stats = stats

        # Screen setup
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.paddle_1 = paddle_1
        self.paddle_2 = paddle_2

        self.prep_lives()

    def prep_lives(self) -> None:
        """Show how many lives are left for each player"""
        self.total_width_1 = 32 * self.stats.lives_left_1
        self.total_width_2 = 32 * self.stats.lives_left_2

        self.lives_1 = Group()
        self.fill_lives(self.lives_1, self.paddle_1, self.stats.lives_left_1, self.total_width_1)

        self.lives_2 = Group()
        self.fill_lives(self.lives_2, self.paddle_2, self.stats.lives_left_2, self.total_width_2)

    def reposition_lives(self) -> None:
        for life_number, life in enumerate(self.lives_1):
            life.rect.x = self.paddle_1.rect.centerx - self.total_width_1 // 2 + life_number * life.rect.width

        for life_number, life in enumerate(self.lives_2):
            life.rect.x = self.paddle_2.rect.centerx - self.total_width_2 // 2 + life_number * life.rect.width

    def fill_lives(self, group: Group, paddle: Paddle, lives_left: int, total_width: int) -> None:
        for life_number in range(lives_left):
            life = Life(self.screen)
            life.rect.y = paddle.rect.y
            life.rect.x = paddle.rect.centerx - total_width // 2 + life_number * life.rect.width
            group.add(life)
