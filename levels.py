import pygame
from settings import PLAYER_COLOR, PLATFORM_COLOR, LEVEL_COLOR, PLAYER_HEIGHT
from level import Level
from elements import Platform,  Door






# Refactor this later
GRASS_LEFT            = (576, 720, 70, 70)
GRASS_RIGHT           = (576, 576, 70, 70)
GRASS_MIDDLE          = (504, 576, 70, 70)
STONE_PLATFORM_LEFT   = (360, 720, 70, 70)
STONE_PLATFORM_MIDDLE = (288, 576, 70, 70)
STONE_PLATFORM_RIGHT  = (360, 576, 70, 70)
DOOR = (70, 0, 70, 70)







# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player, height = 70, screen=None, level_design=None):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player, height=height, screen=screen, level_design=level_design)
    
        # Create platforms with sprites
        level = self.get_level_from_design(using_sprite=True, sprite_left = GRASS_LEFT, sprite_right=GRASS_RIGHT, sprite_center=GRASS_MIDDLE, pos_y=screen.get_rect().height - PLAYER_HEIGHT)
        
        # This is the door level change.
        # =======================================
        door = Door(70, 70, self.level_limit_x, self.level_limit_y, DOOR)
        self.background_sprites.add(door)
        # =======================================

        for platform in level:
            block = Platform(image = platform[4])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

       
 



        


 
# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """
 
    def __init__(self, player, height=70, screen=None, level_design=None):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player, height=height, screen=screen, level_design=level_design)
        
        # Create platforms with sprites
        level = self.get_level_from_design(using_sprite=True, sprite_left = STONE_PLATFORM_LEFT, sprite_right=STONE_PLATFORM_RIGHT, sprite_center=STONE_PLATFORM_MIDDLE, pos_y=screen.get_rect().height - PLAYER_HEIGHT)

        # Add door to finish level
        door = Door(70, 70, self.level_limit_x, self.level_limit_y, DOOR)
        self.background_sprites.add(door)

        # Add door to enter level
        door2 = Door(70, 70, (screen.get_rect().width // 2)-50, screen.get_rect().height - PLAYER_HEIGHT, DOOR)
        self.background_sprites.add(door2)

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(image = platform[4])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 