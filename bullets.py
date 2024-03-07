import pygame

from pygame.sprite import Sprite

class Bullets(Sprite):
    """A class to manage bullets"""

    def __init__(self, ai_game):
        """Creating a bullet obj at ship's current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Creating a bullet rect at (0,0) and then setting correct position
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Storing the bullet's position as a decimal value.
        self.y = float(self.rect.y)


    def update(self):
        """Moving the bullets to upside"""
        # update the decimal position of the bullet
        self.y -= self.settings.bullet_speed

        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Drawing the bullet"""
        pygame.draw.rect(self.screen, self.color, self.rect)