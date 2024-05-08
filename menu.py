import pygame
import pygame.freetype


class Button:
    def __init__(self, screen: pygame.Surface, msg: str) -> None:
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

        self.msg_rect = self.font.render(self.msg, self.text_colour)[1]
        self.msg_rect.center = self.screen_rect.center

    def render(self):
        """Draw the button on the screen"""
        self.screen.fill(self.button_colour, self.rect)
        self.font.render_to(self.screen, self.msg_rect, self.msg, self.text_colour)


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
