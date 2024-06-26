import pygame
from pygame.sprite import Group

from game_stats import GameStats
from settings import Settings
from singleplayer.life import Life


class Scoreboard:
    def __init__(self, screen: pygame.Surface, settings: Settings, stats: GameStats) -> None:
        # Settings setup
        self.settings = settings
        self.stats = stats

        # Screen setup
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.prep_lives()

    def prep_lives(self) -> None:
        """Show how many lives are left"""
        self.lives = Group()
        for life_number in range(self.stats.lives_left_1):
            life = Life(self.screen)
            life.rect.x = 10 + life_number * life.rect.width
            life.rect.y = 10
            self.lives.add(life)

    def score(self) -> None:
        """Increments the score"""
        self.stats.strikes += 1
        self.stats.score += 10 * self.stats.strikes
