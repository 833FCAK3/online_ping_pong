from settings import Settings


class GameStats:
    """Track statistics and game state"""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.reset_stats()

        # Game state
        self.game_active = False
        self.game_started = False

        self.high_score = 0

    def reset_stats(self) -> None:
        self.lives_left_1 = self.settings.total_lives
        self.lives_left_2 = self.settings.total_lives
        self.strikes = 0
        self.vulnerable = True
        self.score = 0
