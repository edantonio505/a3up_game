from elements import Platform, Level
from settings import PLAYER_COLOR, PLATFORM_COLOR, LEVEL_COLOR
 


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player, height = 70, screen=None, level_design=None):
        """ Create level 1. """


        # Call the parent constructor
        Level.__init__(self, player, height=height, screen=screen, level_design=level_design)
        self.level_limit = -1000    
        level = self.get_level_from_design()
    
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], color=PLATFORM_COLOR)
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

        Level.__init__(self, player, height= height, screen=screen, level_design = level_design)
        self.level_limit = -1000
        level = self.get_level_from_design()
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], color=PLATFORM_COLOR)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 