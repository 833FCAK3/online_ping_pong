import pygame
import pygame.freetype


class Button:
    def __init__(self, screen: pygame.Surface, msg: str) -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_colour = (0, 200, 0)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont("None", 48)

        # Build the buttons's rect object, and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg: str) -> None:
        """Turn msg into a rendered image, and center it on the button"""
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def render(self):
        """Draw the button on the screen"""
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Text:
    def __init__(self, screen: pygame.Surface, text: str) -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Text parameters
        self.text_colour = (255, 255, 255)
        self.font = pygame.freetype.SysFont("none", 54)
        self.text = text

        self.rect = self.font.render(self.text, self.text_colour)[1]
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = int(self.screen_rect.height / 5)

    def render(self) -> None:
        """Renders the text to the screen"""
        self.font.render_to(self.screen, self.rect, self.text, self.text_colour)
