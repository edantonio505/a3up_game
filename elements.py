import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, BLACK, PLAYER_HEIGHT, RED, SPRITE_SHEET_PATH


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

        self.walking_frames_l = []
        self.walking_frames_r = []


        # self.image = pygame.Surface([self.width, self.height])
        # self.image.fill(color)
        self.direction = "R"


        sprite_sheet = SpriteSheet("images/p1_walk.png")


        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)
 
        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)



        self.image = self.walking_frames_r[0]
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

        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        
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
        self.direction = "L"
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        self.direction = "R"
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 



class Door(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, sprite_sheet_data=None):
        super().__init__()

        sprite_sheet = SpriteSheet("images/tiles_spritesheet.png")
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y





 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width=None, height=None, color=(0, 255, 0), sprite_sheet_data=None, image=None):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()


        if not image:
            if sprite_sheet_data:   
                sprite_sheet = SpriteSheet("images/tiles_spritesheet.png")
                self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                                sprite_sheet_data[1],
                                                sprite_sheet_data[2],
                                                sprite_sheet_data[3])
                self.image = pygame.transform.scale(self.image, (width, height))
                
            else:
                self.image = pygame.Surface([width, height])
                self.image.fill(color)
        else:
            self.image = image

        self.rect = self.image.get_rect()
    
    def __str__(self):
        message = "Platform:\n"
        message += "\tpos_x: {}\n".format(self.rect.x)
        message += "\tpos_y: {}\n".format(self.rect.y)
        return message


















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







    def get_platform_image_sprite(self, sprite_sheet, platform_level, block_width, sprite_coord):
        image = pygame.Surface([70, 70]).convert()
        image.set_colorkey(RED)
        image.blit(sprite_sheet, (0, 0), sprite_coord)
        image = pygame.transform.scale(image, (block_width, platform_level[1]))
        return image








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










class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
 
    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """
 
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
 
 
    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
 
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
 
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
 
        # Assuming black works as the transparent color
        image.set_colorkey(BLACK)
 
        # Return the image
        return image


 