import pygame
from pygame.sprite import Sprite


class Life(Sprite):
    def __init__(self, screen: pygame.Surface) -> None:
        super(Life, self).__init__()

        # Screen setup
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Get the life image, scale it down and get its rect
        self.image = pygame.image.load("multiplayer/images/life.png")
        self.image = pygame.transform.scale(self.image, (32, 29))
        self.rect = self.image.get_rect()
