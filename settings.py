from typing import Tuple

import pygame


class Settings:
    """A class to store all settings for the game"""

    def __init__(self) -> None:
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 750
        self.screen_height = 570
        self.max_rez, self.display = self.detect_highest_resolution_display()
        self.bg_colour = (200, 200, 200)
        self.fps = 60
        self.fps_adjusment = self.fps // 60

        # Paddle settings
        self.paddle_width, self.paddle_height = 330, 40
        self.paddle_colour = (0, 255, 0)
        self.paddle_speed = 35

        # Ball settings
        self.ball_width, self.ball_height = 50, 50
        self.ball_colour = (0, 0, 0)
        self.ball_speed = 6
        self.speed_up_factor = 1.05

        # Game settings
        self.total_lives = 3

        # Connection settings
        self.server_host = "localhost"
        self.server_port = 5555

    def detect_highest_resolution_display(self) -> Tuple[Tuple[int, int], int]:
        """Finds the highest available resolution"""
        display_resolutions = pygame.display.get_desktop_sizes()
        max_rez = max(display_resolutions)
        index = display_resolutions.index(max(display_resolutions))
        return max_rez, index
