class Settings:
    """A class to store all settings for the game"""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 600
        self.bg_colour = (200, 200, 200)
        self.fps = 60

        # Paddle settings
        self.paddle_width, self.paddle_height = 180, 25
        self.paddle_colour = (0, 255, 0)
        self.paddle_speed = 1

        # ball settings
        self.ball_width, self.ball_height = 50, 50
        self.ball_colour = (0, 0, 0)
        self.ball_speed = 1
