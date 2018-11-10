import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
 
    # -- Methods
    def __init__(self, height=40, width=60, color=(255, 0, 0)):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.width = width
        self.height = height
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(color)

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

            
        # List of sprites we can bump against
        self.level = None
        self.player_over_threshold = False
        self.died = False



    def __str__(self):
        message = "Player: \n"
        message += "\theight: {}\n".format(self.height)
        message += "\twidth: {}\n".format(self.width)
        message += "\tpos_x: {}\n".format(self.rect.x)
        message += "\tpos_y: {}\n".format(self.rect.y)
        return message
    
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.player_over_threshold == False:
            if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
                self.change_y = 0
                self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
















 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height, color=(0, 255, 0)):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
    
    def __str__(self):
        message = "Platform:\n"
        message += "\tpos_x: {}\n".format(self.rect.x)
        message += "\tpos_y: {}\n".format(self.rect.y)



















class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player, height=70, screen = None, level_design = None):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.height = height
        
        if not screen:
            print("Screen needed in level")
            quit()

        if not level_design:
            print("level design needed")
            quit()

        self.level_design = level_design
        self.screen_height = screen.get_rect().height
        self.screen_width = screen.get_rect().width

        # How far this world has been scrolled left/right
        self.world_shift = 0
    

    def __str__(self):
        message = "Level: \n"
        message += "\tplatform_list: {}\n".format(self.platform_list)
        message += "\twold_shift: {}\n".format(self.world_shift)
        message += "\tplayer_over_threshold: {}\n".format(self.player_over_threshold)
        message += "\tlevel_design: {}\n".format(self.level_design)
        return message




    def get_level_from_design(self):
        level = []
        platform_height = self.height
        level_design = self.level_design.split("\n")
        pos_y = 520
        
        for platform in reversed(level_design[1:-2]):
            new_platform = None
            platform = platform[1:-1]
            if "#" in platform:
                new_platform = []
                platform_width = 0
                pos_x = 0     
                block_width = (self.screen_width //  len(platform))
                first_block = 0

                for i in range(len(platform)):
                    if first_block == 0 and platform[i] == " ":
                        pos_x += block_width

                    if platform[i] == "#":
                        if first_block == 0:
                            first_block = i
                        platform_width += block_width
                
                new_platform = [platform_width, platform_height, pos_x, pos_y]
                pos_y -= platform_height
            else:
               pos_y -= platform_height

            if new_platform:
                level.append(new_platform)
        return level



    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen, color=(0, 0, 255)):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(color)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_y, screen):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift += shift_y
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.y -= shift_y

            if platform.rect.y >= screen.get_rect().height:
                self.platform_list.remove(platform)

        for enemy in self.enemy_list:
            enemy.rect.y -= shift_y
 