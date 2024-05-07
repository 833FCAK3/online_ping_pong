import pygame


class Button:
    def __init__(self, screen: pygame.Surface, msg: str) -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Dimensions and properties of the paddle
        self.width, self.height = 200, 50
        self.button_colour = (0, 200, 0)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the paddle's rect object, and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg: str) -> None:
        """Turn msg into a rendered image, and center text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def render(self):
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
