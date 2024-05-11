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
        self.width, self.height = self.settings.ball_width, self.settings.ball_height
        self.ball_colour = self.settings.ball_colour

        # Build the ball's rect object
        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # Randomize starting direction
        self.moving_left = choice([False, True])
        self.moving_right = not self.moving_left
        self.moving_down = choice([False, True])
        self.moving_up = not self.moving_down

    def randomize_initial_coords(self) -> None:
        """Returns two random numbers within limits of screen resolution"""
        self.x = randint(self.screen_rect.left + self.width, self.screen_rect.right - self.width)
        self.y = randint(self.screen_rect.top, int(self.screen_rect.bottom / 4))

    def respawn_ball(self) -> None:
        """Respawns the ball at random location at the top part of the screen"""
        self.randomize_initial_coords()
        self.rect.left, self.rect.top = self.x, self.y

    def update_position(self) -> None:
        """Update the balls's position, based on movement flags"""
        if self.frame % self.settings.fps_adjusment == 0:  # Slows down the ball to ~ 60 fps speed
            # Adjust horizontal position
            if self.moving_left and self.rect.left > self.screen_rect.left:
                self.x -= self.settings.ball_speed
            elif self.moving_right and self.rect.right < self.screen_rect.right:
                self.x += self.settings.ball_speed

            # Adjust vertical position
            if self.moving_up and self.rect.top > self.screen_rect.top:
                self.y -= self.settings.ball_speed
            elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
                self.y += self.settings.ball_speed

            self.rect.x, self.rect.y = int(self.x), int(self.y)

            # Unstuck the ball from outside the screen borders
            if self.rect.left < self.screen_rect.left:
                self.rect.left = self.screen_rect.left
            elif self.rect.right > self.screen_rect.right:
                self.rect.right = self.screen_rect.right
            if self.rect.top < self.screen_rect.top:
                self.rect.top = self.screen_rect.top

        self.frame += 1

    def render(self) -> None:
        """Draw the ball at its current location"""
        pygame.draw.rect(self.screen, self.ball_colour, self.rect)
