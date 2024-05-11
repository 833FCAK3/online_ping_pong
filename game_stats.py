from settings import Settings


class GameStats:
    """Track statistics and game state"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.reset_stats()

        # Game state
        self.game_active = False
        self.game_started = False
        self.direction_speed_change_lock = False

    def reset_stats(self):
        self.lives_left = self.settings.total_lives
        self.vulnerable = True
