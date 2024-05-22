import pygame
import pygame.freetype

from menu import BaseText, Button, GameJoever
from singleplayer.game_stats import GameStats


class Score(BaseText):
    def __init__(self, screen: pygame.Surface, stats: GameStats) -> None:
        super(Score, self).__init__(screen, 54)
        self.stats = stats
        self.reposition()

    def reposition(self) -> None:
        self.msg = str(self.stats.score)

        self.rect = self.font.render(self.msg, self.text_colour)[1]
        self.rect.right = self.screen_rect.right - 25
        self.rect.centery = int(self.screen_rect.top + 40)


class HighScore(BaseText):
    def __init__(self, screen: pygame.Surface, stats: GameStats) -> None:
        super(HighScore, self).__init__(screen, 54)
        self.stats = stats
        self.reposition()

    def reposition(self) -> None:
        self.msg = str(self.stats.high_score)

        self.rect = self.font.render(self.msg, self.text_colour)[1]
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = int(self.screen_rect.height / 3)
