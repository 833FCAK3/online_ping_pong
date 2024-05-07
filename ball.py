from random import choice, randint

import pygame

from settings import Settings


class Ball:
    def __init__(self, screen: pygame.Surface, settings: Settings) -> None:
        """Initialize the ball and set its starting position and movement direction"""
        self.settings = settings

        # Screen setup
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.frame = 0

        # Dimensions and properties of the paddle, randomize starting position
        self.x = randint(self.screen_rect.left, self.screen_rect.right)
        self.y = randint(self.screen_rect.top, int(self.screen_rect.bottom / 4))
        self.width, self.height = self.settings.ball_width, self.settings.ball_height
        self.ball_colour = self.settings.ball_colour

        # Build the ball's rect object
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Randomize starting direction
        self.moving_left = choice([False, True])
        self.moving_right = not self.moving_left
        self.moving_down = choice([False, True])
        self.moving_up = not self.moving_down

    def render(self) -> None:
        """Draw the ball at its current location"""
        pygame.draw.rect(self.screen, self.ball_colour, self.rect)

    def update_position_env(self) -> None:
        """Update the balls's position, based on movement flags"""
        if self.frame % 7 == 0:  # Slows down the ball
            if self.moving_left and self.rect.left > self.screen_rect.left:
                self.rect.x -= 1
            elif self.moving_right and self.rect.right < self.screen_rect.right:
                self.rect.x += 1

            if self.moving_up and self.rect.top > self.screen_rect.top:
                self.rect.y -= 1
            elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
                self.rect.y += 1

            if self.rect.left == self.screen_rect.left:
                self.moving_left, self.moving_right = False, True
            if self.rect.right == self.screen_rect.right:
                self.moving_left, self.moving_right = True, False
            if self.rect.top == self.screen_rect.top:
                self.moving_up, self.moving_down = False, True

        self.frame += 1
