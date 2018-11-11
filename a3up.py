import pygame
from settings import *
from levels import *
from level_designs import *
from elements import Player


 
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption(WINDOW_TITLE)
 
    # Create the player
    player = Player(PLAYER_HEIGHT, PLAYER_WIDTH, color=PLAYER_COLOR)
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player, height=PLATFORM_HEIGHT, screen=screen, level_design=level1))
    level_list.append(Level_02(player, height=PLATFORM_HEIGHT, screen=screen, level_design=level2))
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    

    x_center = (SCREEN_WIDTH // 2) - (PLAYER_HEIGHT // 2)

    player.rect.x = x_center
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
                highest_jump = top_diff_threshosld+HIGHEST_JUMP_RATE
            else:
                highest_jump += HIGHEST_JUMP_RATE
            current_level.shift_world(-1*(HIGHEST_JUMP_RATE), screen)
            player.rect.top = top_diff_threshosld
        
        if highest_jump >= HIGHEST_JUMP_THRESHOLD:
            player.player_over_threshold = True


        if player.rect.top >= (screen.get_rect().height) and player.player_over_threshold == True:
            print("player lost")
            running = False

        current_position_y = player.rect.y + current_level.world_shift
        current_position_x = player.rect.x

        if player.rect.x > SCREEN_WIDTH:
            player.rect.x = 0


        elif player.rect.x < -(player.rect.width):
            player.rect.x = SCREEN_WIDTH



        if current_level.level_limit_x != None and current_level.level_limit_y != None:
            if current_position_x in range(current_level.level_limit_x, current_level.level_limit_x+PLAYER_WIDTH) \
            and current_position_y in range(current_level.level_limit_y - player.rect.height, current_level.level_limit_y):
            
                player.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
                player.rect.x = x_center
                player.player_over_threshold = False
                highest_jump = 0
                if current_level_no < len(level_list)-1:
                    current_level_no += 1
                    current_level = level_list[current_level_no]
                    player.level = current_level
                    
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
