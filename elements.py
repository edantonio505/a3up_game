import pygame
from settings import BLACK

# ==========================================================================
#                       DOOR TO SPAWN PLAYER OR TO END LEVEL
# ==========================================================================
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








# ==========================================================================
#                    PLATFORM OBJECT
# ==========================================================================
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








# ==========================================================================
#                SPRITEHSEET OBJECT OT GET GAME OBJECTS IMAGES
# ==========================================================================
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


 