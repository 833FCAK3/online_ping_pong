import pygame
import pygame.freetype

from menu import BaseText, Button, GameJoever
from two_players.game_stats import GameStats


class Strikes(BaseText):
    def __init__(self, screen: pygame.Surface, stats: GameStats) -> None:
        super(Strikes, self).__init__(screen, 35)
        self.stats = stats
        self.msg = ""

    def render(self) -> None:
        """Renders the msg to the screen"""
        if not self.msg:
            self.msg = "Total strikes: " + str(self.stats.strikes)
        self.rect = self.font.render(self.msg, self.text_colour)[1]
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = int(self.screen_rect.height / 12 * 5)

        self.font.render_to(self.screen, self.rect, self.msg, self.text_colour)
