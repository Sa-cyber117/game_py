import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """A 'ship' class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #   Pygame treats every game element as a rectangle
        self.screen_rect = ai_game.screen.get_rect()

        #   Add ship image and get its rect
        self.image = pygame.image.load("images/ship_1.bmp")

        #   here we are gonna get the coordinates of the rect_image
        self.rect =self.image.get_rect()

        #   It'll be starting position for the ship every time
        #   For midbottom:
        self.rect.midbottom = self.screen_rect.midbottom
        # self.rect.center = self.screen_rect.center
        
        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movenent Flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Updating the ships position based on Movenent Flag"""
        # Update the ship's x value, not the rect.        
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        if self.moving_up and self.rect.top >0 :
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x        
        self.rect.y = self.y        


    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """ Create the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)