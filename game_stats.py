
class GameStats:
    """Tracking statistics of the game"""

    def __init__(self, ai_game):
        """ Init statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Start in an inactive mode
        self.game_active = False

        # High score should never get reset
        self.high_score = 0

    def reset_stats(self):
        """Giving 3 lives"""
        self.ships_left = self.settings.ship_limit
        self.score = 0 
        self.level = 1
        