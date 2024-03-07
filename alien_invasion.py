import sys
import pygame
from settings import Settings
from ship import Ship
from bullets import Bullets
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button
from score import Score

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""

        pygame.init()
        self.settings = Settings()

        #   Setting Display Size and heading caption
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height))
        
        # For full screen mode
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width= self.screen.get_rect().width
        self.settings.screen_height= self.screen.get_rect().height


        # Create an instance to store game stats
        self.stats = GameStats(self)
        self.score_board = Score(self)

        pygame.display.set_caption("Alien Invasoin")
        self.ship= Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._creating_fleet()

        self.play_button = Button(self,"Play")

        #   Setting background color
        self.bg_color = (self.settings.bg_color)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            #   Tracking keyboard and mouse events.
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                # self.bullets.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            #   Getting rid of the unwanted bullets
            # for bullet in self.bullets.copy():
            #      if bullet.rect.bottom <= 0:
            #           self.bullets.remove(bullet)
            # print(len(self.bullets))


    
    def _check_events(self):
            #   Here event is a sub-module and get() is a function
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)

                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)


                elif event.type == pygame.MOUSEBUTTONDOWN:
                     mouse_pos = pygame.mouse.get_pos()
                     self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
         """Responding to mouse click"""
         button_clicked = self.play_button.rect.collidepoint(mouse_pos)
         if button_clicked and not self.stats.game_active:
              # Resetting the game settings
              self.settings.initialize_dynamic_settings()
              self.stats.reset_stats()
              self.stats.game_active = True

              self.score_board.prep_score()
              self.score_board.prep_level()
              self.score_board.prep_ships()

              # Get rid of unnecessry aliens and bullets
              self.aliens.empty()
              self.bullets.empty()

              # Creating a new fleet and aligning the ship
              self._creating_fleet()
              self.ship.center_ship()
              # Hiding cursor    
              pygame.mouse.set_visible(False)

    
    def _check_keydown_events(self,event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            #  self.space_pressed = True
             self._fire_bullet()
        # elif event.key == pygame.K_p:
        #      self._
        


    def _check_keyup_events(self,event):
        """Respond to keyreleases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right =False
        elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False
        elif event.key == pygame.K_UP:
                self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
                self.ship.moving_down = False

   

    def _update_screen(self):
            """Update images on the screen, and flip to the new screen."""

            self.screen.fill(self.bg_color)
            #  Games do not load everything like we imagine. It just renders
            #  newly rendered screen per second. It's not what you think.
            #  Here we have to show the most recently drawned screen.
            #  Here self.screen is an instace of pyg.Surface class(an object) 
            #  and 'fill()' is a method of pyg.Surface

            self.ship.blitme()

            for bullet in self.bullets.sprites():
                 bullet.draw_bullet() 

            self.aliens.draw(self.screen) 

            # Draw the score
            self.score_board.show_score()

            if not self.stats.game_active:
                 self.play_button.draw_button()

            
                 
            pygame.display.flip()
            
    def _fire_bullet (self):
        """Creating a new bullet and adding it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullets(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of the bullets and get rid of old bullets"""
        # update bullet position
        self.bullets.update()

        # getting rid of bullets that are gone
        for bullet in self.bullets.copy():
             if bullet.rect.bottom <= 0:
                  self.bullets.remove(bullet)
        
        self._check_bullets_aliens_collisions()


    def _check_bullets_aliens_collisions(self):
        # Check for any bullets that's overlaping with alien ship
        # then get rid of that bullet and ship
        collisions= pygame.sprite.groupcollide(
             self.bullets, self.aliens, True, True)
        
        if not self.aliens:
             # Destroy existing bullets and create a new crew
             self.bullets.empty()
             self._creating_fleet()
             self.settings.increase_speed()

             # Increase level 
             self.stats.level += 1
             self.score_board.prep_level()
             
        if collisions:
             for aliens in collisions.values():
                 self.stats.score += self.settings.kill_point * len(aliens)

             self.score_board.prep_score() 
             self.score_board.check_high_score()



    def _creating_fleet(self):
        """Creting multiple alien ships"""
        # make alien fleet
        alien = Alien(self)
        alien_width, alien_height  = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)


        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                             (4 * alien_height) - (2*ship_height))

        number_rows = available_space_y//(2*alien_height)

        # Creating whole fleet
        for row_number in range(number_rows):    
            # Creating the 1st row of alien_ship
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number,row_number)


    def _create_alien(self, alien_number, row_number):
        """Creating an alien and placing it in a row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        # alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
         """ When fleet touches edge of the screen"""
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break
    
    def _change_fleet_direction(self):
        """ Drop the entire fleet and  change the direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 
        

    def _update_aliens(self):
         """Update the positions of all aliens"""
         self._check_fleet_edges()
         self.aliens.update()

         # Check for the alien and ship collision
         if pygame.sprite.spritecollideany( self.ship, self.aliens):
            #   print("Game over!")
            #   sys.exit()
            self._ship_hit()
        
         self._check_aliens_bottom()

    def _ship_hit(self):
        """ Alien hits the ship"""
        if self.stats.ships_left > 0: 
            # Decrement ships_left & update ship_number
            self.stats.ships_left -= 1
            self.score_board.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            #  self._create_fleet()
            self._creating_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """ check if any ship hits the bottom"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

if __name__ == "__main__":
    #   Run the game creating an instance
    ai = AlienInvasion()                    
    ai.run_game()

