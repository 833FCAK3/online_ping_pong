import pygame


class Paddle:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Dimensions and properties of the paddle
        self.width, self.height = 150, 25
        self.paddle_colour = (0, 255, 0)
        self.x = self.screen_rect.centerx - self.width / 2
        self.y = self.screen_rect.bottom - self.height

        # Build the paddle's rect object, and center it
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Movement flags
        self.moving_left = False
        self.moving_right = False

    def render(self):
        pygame.draw.rect(self.screen, self.paddle_colour, self.rect)

    def update_position(self):
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.rect.x -= 1
        elif self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += 1
