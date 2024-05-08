import pygame
import pygame.freetype

from game_stats import GameStats


class Button:
    def __init__(self, screen: pygame.Surface, stats: GameStats, msg: str, alt_msg: str = "") -> None:
        self.stats = stats
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Dimensions and properties of the button
        self.width, self.height = 220, 60
        self.button_colour = (0, 200, 0)
        self.text_colour = (255, 255, 255)

        self.font = pygame.freetype.SysFont("None", 48)

        # Build the buttons's rect object, and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.msg = msg
        self.alt_msg = alt_msg

        self.msg_rect = self.font.render(self.msg, self.text_colour)[1]
        self.msg_rect.center = self.screen_rect.center
        self.alt_msg_rect = self.font.render(self.alt_msg, self.text_colour)[1]
        self.alt_msg_rect.center = self.screen_rect.center

    def render(self):
        """Draw the button on the screen"""
        text = self.msg if self.stats.game_started else self.alt_msg
        rect = self.msg_rect if self.stats.game_started else self.alt_msg_rect

        self.screen.fill(self.button_colour, self.rect)
        self.font.render_to(self.screen, rect, text, self.text_colour)


class Text:
    def __init__(self, screen: pygame.Surface, msg: str) -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Text parameters
        self.text_colour = (255, 255, 255)
        self.font = pygame.freetype.SysFont("None", 54)
        self.msg = msg

        self.rect = self.font.render(self.msg, self.text_colour)[1]
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = int(self.screen_rect.height / 5)

    def render(self) -> None:
        """Renders the msg to the screen"""
        self.font.render_to(self.screen, self.rect, self.msg, self.text_colour)
