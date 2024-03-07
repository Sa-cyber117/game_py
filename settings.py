class Settings:
    """Creating a setting class to store all the srttings for the game."""

    def __init__(self):
        """Initializing the game settings"""

        #   Screen settings like height and width, background color
        self.screen_width = 860
        self.screen_height = 600
        self.bg_color = (20, 20, 20)

        #   Ship speed
        self.ship_limit = 3

        #   Bullets
        # self.bullet_speed = 1.5
        self.bullet_width = 2
        self.bullet_height = 10
        self.bullet_color = (255,80,90)
        self.bullets_allowed = 15

        #   Alien settings
        self.fleet_drop_speed = 10

        # Game speed up
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.alien_speed = 0.8
        self.bullet_speed = 2.0
        self.ship_speed = 1.0
        self.kill_point = 10

        #   fleet_direction : +-1 -> right,left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed as level"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

        # Increasing points
        self.kill_point = int(self.kill_point * self.score_scale)
        print(self.kill_point)