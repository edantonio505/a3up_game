
import pygame
from settings import RED, BLACK, SPRITE_SHEET_PATH, SCREEN_HEIGHT, PLAYER_HEIGHT



# ==========================================================================
#                           LEVEL OBJECT
#          This will instantiate a level object and render level design
# ==========================================================================
class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player, height=70, screen = None, level_design = None):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.player = player
        self.height = height
        self.level_limit_x = None
        self.level_limit_y = None

        if not screen:
            print("Screen needed in level")
            quit()
        else:
            self.screen = screen
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


    # Get positin X of multiple platforms
    def get_width_posx_multiple_platform(self, platform, block_width):
        first_block = 0
        posx_array = []
        width_array = []
        posx = 0    
        for i in range(len(platform)):
            platform_width = 0
            try:
                if platform[i] == " " and platform[i+1] == "#":
                    posx = (i+1)*block_width
                    posx_array.append(posx)
            except:
                pass
        count = 0
        for i in range(len(platform)):
            if platform[i] == "#":
                count += block_width
            elif platform[i] == " ":
                if count > 0:
                    width_array.append(count)
                count = 0
        return zip(width_array, posx_array)





    # Returns a list of platforms [width, height, posistion X, position Y)
    def get_platform_list(self, platform, platform_width,  platform_height,  pos_x, pos_y, block_width, number_of_platforms):
        first_block = 0
        posx_width = None
        if number_of_platforms > 1:
            platforms = []
            posx_width = self.get_width_posx_multiple_platform(platform, block_width)
            for width, posx in posx_width:
                platforms.append([width, platform_height,  posx, pos_y])
            return platforms
        for i in range(len(platform)):
            if first_block == 0 and platform[i] == " ":
                pos_x += block_width

            if platform[i] == "@":
                if first_block == 0:
                    first_block = i
                platform_width += block_width

            if platform[i] == "#":
                if first_block == 0:
                    first_block = i
                platform_width += block_width
        return [platform_width, platform_height, pos_x, pos_y]






    # Returns an block image to apply to a new platform element for sprite
    def get_platform_image_sprite(self, sprite_sheet, platform_level, block_width, sprite_coord):
        image = pygame.Surface([70, 70]).convert()
        image.set_colorkey(RED)
        image.blit(sprite_sheet, (0, 0), sprite_coord)
        image = pygame.transform.scale(image, (block_width, platform_level[1]))
        return image







    # returns a list of all platforms list included in level design
    def get_level_platform_elements(self, block_width, pos_y):
        level = []
        platform_height = self.height
        level_design = self.level_design.split("\n")
        for platform in reversed(level_design[1:-2]): 
            new_platform = None
            platform = platform[1:-1]
            number_of_platforms = len(platform.split())
            if "#" in platform:
                new_platform = []
                platform_width = 0
                pos_x = 0     
                block_width = (self.screen_width //  len(platform))
                new_platform = self.get_platform_list(platform, platform_width,  platform_height,  pos_x, pos_y, block_width, number_of_platforms)
                pos_y -= platform_height
            elif "@" in platform:
                new_platform = []
                platform_width = 0
                pos_x = 0
                block_width = (self.screen_width //  len(platform))
                new_platform = self.get_platform_list(platform, platform_width,  platform_height,  pos_x, pos_y, block_width, number_of_platforms)
                self.level_limit_y = new_platform[3]
                self.level_limit_x = new_platform[2]
                new_platform = None
            else:
               pos_y -= platform_height
            if new_platform:
                if number_of_platforms > 1:
                    for platform in new_platform:
                        level.append(platform)
                else:
                    level.append(new_platform)
        return level, block_width








    # It returns all images with all platforms lists to add to platform objects and render the in the game
    def get_platforms_with_sprites(self, level, block_width, sprite_right, sprite_left, sprite_center):
        sprite_level = []
        # full platform width
        file_path = SPRITE_SHEET_PATH
        # load image
        sprite_sheet = pygame.image.load(file_path).convert()
        # ===================================================
        for platform_level in level:
            if platform_level[0] > block_width:
                current_block_pos = 0
                # Create a new blank platform
                image = pygame.Surface([platform_level[0], platform_level[1]]).convert()
                image.set_colorkey(BLACK)

                # blit left side onto new platform
                image.blit(self.get_platform_image_sprite(sprite_sheet, platform_level, block_width, sprite_left), (current_block_pos, 0))
                current_block_pos += block_width

                # blit sprite onto center for platform
                number_of_blocks_center = (platform_level[0] - (block_width*2)) // block_width
                if number_of_blocks_center > 0:            
                    image_block_center = self.get_platform_image_sprite(sprite_sheet, platform_level, block_width, sprite_center)
                    for posx_block in range(number_of_blocks_center):
                        image.blit(image_block_center, (current_block_pos, 0))
                        current_block_pos += block_width

                # blit right sprite onto right side of platform
                image.blit(self.get_platform_image_sprite(sprite_sheet, platform_level, block_width, sprite_right), (current_block_pos, 0))
                platform_level.append(image)
                sprite_level.append(platform_level)
            else:
                image = pygame.Surface([platform_level[0], platform_level[1]]).convert()
                image.set_colorkey(BLACK)
                 # blit sprite onto center for platform
                image.blit(self.get_platform_image_sprite(sprite_sheet, platform_level, block_width, sprite_center), (0, 0))
                platform_level.append(image)
                sprite_level.append(platform_level)
        return sprite_level








    # convert level design to platforms array with [width, height, pos_x_pos_y] values
    def get_level_from_design(self, using_sprite=False, sprite_right=None, sprite_left=None, sprite_center=None, pos_y = (SCREEN_HEIGHT-PLAYER_HEIGHT)):        
        block_width = 0
        level, block_width = self.get_level_platform_elements(block_width, pos_y)
        if using_sprite and block_width > 0:
           level = self.get_platforms_with_sprites(level, block_width, sprite_right, sprite_left, sprite_center)
        return level





    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.background_sprites.update()
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen, color=(0, 0, 255)):
        """ Draw everything on this level. """
        # Draw the background
        screen.fill(color)
        # Draw all the sprite lists that we have
        self.background_sprites.draw(screen)
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

        for sprite in self.background_sprites:
            sprite.rect.y -= shift_y




