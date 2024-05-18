import pygame

from multiplayer.settings import Settings


class Paddle:
    def __init__(self, settings: Settings, player_number: int) -> None:
        """Initialize the ball and set its starting position"""
        self.settings = settings

        self.player_number = player_number

        # Movement flags
        self.moving_left = False
        self.moving_right = False

    def center_paddle(self) -> None:
        """Center the paddle on the screen"""
        self.x = int(self.screen_rect.centerx - self.width / 2)

    def update_position(self) -> None:
        """Update the paddle's position, based on movement flags"""
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.paddle_speed
        elif self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.paddle_speed

        self.rect.x = int(self.x)

    def set_screen(self, screen: pygame.Surface):
        # Screen setup
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Dimensions and properties of the paddle
        self.width, self.height = self.settings.paddle_width, self.settings.paddle_height
        self.paddle_colour = self.settings.paddle_colour
        self.x = self.screen_rect.centerx - self.width / 2

        if self.player_number == 1:
            self.y = self.screen_rect.bottom - self.height
        elif self.player_number == 2:
            self.y = self.screen_rect.top

        # Build the paddle's rect object
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self) -> None:
        """Draw the paddle at its current location"""
        pygame.draw.rect(self.screen, self.paddle_colour, self.rect)
