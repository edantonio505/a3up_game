import pygame
from settings import *
from levels import *
from elements import Player


 
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Side-scrolling Platformer")
 
    # Create the player
    player = Player(PLAYER_HEIGHT, PLAYER_WIDTH, color=PLAYER_COLOR)
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = (SCREEN_WIDTH // 2) - (PLAYER_HEIGHT // 2)
    player.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
    active_sprite_list.add(player)
    running = True

    # Calculate highest jump
    highest_jump = 0
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    

    # -------- Main Program Loop -----------
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_SPACE:
                    player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop() 
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
        top_diff_threshosld = 200

        # Move screen while jumping
        if player.rect.top < top_diff_threshosld:
            diff = player.rect.top + top_diff_threshosld
            player.rect.top = top_diff_threshosld

            if highest_jump == 0:
                highest_jump = top_diff_threshosld+10
            else:
                highest_jump += 10
            current_level.shift_world(-10, screen)
            player.rect.top = top_diff_threshosld
        
        if highest_jump >= 450:
            player.player_over_threshold = True

        if player.rect.top >= (520+PLAYER_HEIGHT) and player.player_over_threshold == True:
            print("player lost")
            running = False

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen, color=LEVEL_COLOR)
        active_sprite_list.draw(screen)
 
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(FPS)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()
