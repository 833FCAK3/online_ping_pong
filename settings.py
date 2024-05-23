from typing import Tuple

import pygame
import yaml


config = yaml.safe_load(open("settings.yml"))
print(config)


class Settings:
    """A class to store all settings for the game"""

    def __init__(self) -> None:
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = config["screen_width"]
        self.screen_height = config["screen_height"]
        self.max_rez, self.display = self.detect_highest_resolution_display()
        self.bg_colour = tuple(config["bg_colour"])
        print(self.bg_colour, type(self.bg_colour))
        self.fps = config["fps"]
        self.fps_adjusment = self.fps // 60

        # Paddle settings
        self.paddle_width, self.paddle_height = config["paddle_width"], config["paddle_height"]
        self.paddle_colour = tuple(config["paddle_colour"])
        self.paddle_speed = config["paddle_speed"]

        # Ball settings
        self.ball_width, self.ball_height = config["ball_width"], config["ball_height"]
        self.ball_colour = tuple(config["ball_colour"])
        self.ball_speed = config["ball_speed"]
        self.speed_up_factor = config["speed_up_factor"]

        # Game settings
        self.total_lives = config["total_lives"]

        # Connection settings
        self.server_host = config["server_host"]
        self.server_port = config["server_port"]

    def detect_highest_resolution_display(self) -> Tuple[Tuple[int, int], int]:
        """Finds the highest available resolution"""
        display_resolutions = pygame.display.get_desktop_sizes()
        max_rez = max(display_resolutions)
        index = display_resolutions.index(max(display_resolutions))
        return max_rez, index
