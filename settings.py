class Settings:
    """A class to store all settings for the game"""

    def __init__(self):
        """Initialize the game's static settings"""
        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_colour = (200, 200, 200)
        self.fps = 60
        self.fps_adjusment = self.fps // 60

        # Paddle settings
        self.paddle_width, self.paddle_height = 300, 40
        self.paddle_colour = (0, 255, 0)
        self.paddle_speed = 30

        # Ball settings
        self.ball_width, self.ball_height = 50, 50
        self.ball_colour = (0, 0, 0)
        self.ball_speed = 6.5
        self.speed_up_factor = 1.05

        # Game settings
        self.total_lives = 3
