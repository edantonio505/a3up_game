from elements import Platform, Level
from settings import PLAYER_COLOR, PLATFORM_COLOR, LEVEL_COLOR
 

# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -5000
 
        # Array with width, height, x, and y of platform
        level = [
            [210, 70, 500, 500],
            [210, 70, 200, 400],
            [210, 70, 100, 300],
            [210, 70, 500, 200],
            [150, 70, 200, 60],
            [210, 70, 500, -20],
            [180, 70, 250, -150],
            [210, 70, 150, -350],
            [180, 70, 500, -550],
            [300, 70, 100, -700],
            [200, 70, 350, -900]
        ]
 
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
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -1000
 
        # Array with type of platform, and x, y location of the platform.
        level = [[210, 30, 450, 570],
                 [210, 30, 850, 420],
                 [210, 30, 1000, 520],
                 [210, 30, 1120, 280],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1], color=PLATFORM_COLOR)
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 