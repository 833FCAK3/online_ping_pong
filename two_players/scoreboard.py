import pygame
from pygame.sprite import Group

from two_players.game_stats import GameStats
from two_players.life import Life
from two_players.paddle import Paddle
from two_players.settings import Settings


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

        self.total_width = 32 * self.stats.lives_left

        self.prep_lives()

    def prep_lives(self) -> None:
        """Show how many lives are left for each player"""
        self.lives_1 = Group()
        for life_number in range(self.stats.lives_left):
            life = Life(self.screen)
            life.rect.y = self.paddle_1.rect.y
            life.rect.x = self.paddle_1.rect.centerx - self.total_width // 2 + life_number * life.rect.width
            self.lives_1.add(life)

        self.lives_2 = Group()
        for life_number in range(self.stats.lives_left):
            life = Life(self.screen)
            life.rect.y = self.paddle_2.rect.y
            life.rect.x = self.paddle_2.rect.centerx - self.total_width // 2 + life_number * life.rect.width
            self.lives_2.add(life)

    def reposition_lives(self):
        for life_number, life in enumerate(self.lives_1):
            life.rect.x = self.paddle_1.rect.centerx - self.total_width // 2 + life_number * life.rect.width

        for life_number, life in enumerate(self.lives_2):
            life.rect.x = self.paddle_2.rect.centerx - self.total_width // 2 + life_number * life.rect.width
