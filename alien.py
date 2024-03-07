import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to manage the alien ship"""

    def __init__(self, ai_geme):
        """init the alien class and setting its starting position"""

        super().__init__()
        self.screen = ai_geme.screen
        self.settings = ai_geme.settings

        # loading the alien image and set its rect attribute
        self.image = pygame.image.load(
            'images/alien-ship1-Photoroom.png-Photoroom.bmp')
        self.rect = self.image.get_rect()

        # starting each new alien near the top of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Storing the alien's exact horizontal location 
        self.x = float(self.rect.x)

    def check_edges(self):
        """Rreturn true if alien is at edge of the screen"""
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right or self.rect.left<=0:
            return True

    def update(self):
        """Move the alien ship to right and left"""
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x
        # self.x -= self.settings.alien_speed
        # self.rect.x = self.x


    