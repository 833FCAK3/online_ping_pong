import pygame
from pygame.sprite import Sprite

from utils import make_path


class Life(Sprite):
    def __init__(self, screen: pygame.Surface) -> None:
        super(Life, self).__init__()

        # Screen setup
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Get the life image, scale it down and get its rect
        path = make_path("two_players/images/life.png")
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, (32, 29))
        self.rect = self.image.get_rect()
