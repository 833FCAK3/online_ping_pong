import pygame
import pygame.freetype

from menu import BaseText, Button, GameJoever
from multiplayer.game_stats import GameStats


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


class Arrow:
    def __init__(self, screen: pygame.Surface, player_number: int) -> None:
        # Screen setup
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Get the arrow image, get its rect
        self.image = pygame.image.load("multiplayer/images/arrow.png")
        self.rect = self.image.get_rect()
        self.blit_to = [self.screen_rect.centerx - self.rect.width / 2, 0]

        if player_number == 1:
            self.blit_to[1] = self.screen_rect.height - self.rect.height
        elif player_number == 2:
            self.image = pygame.transform.rotate(self.image, 180)

    def render(self) -> None:
        self.screen.blit(self.image, self.blit_to)
