import pygame
import sys



def main():
	pygame.init()
	pygame.display.set_caption("First actual game")

	# WINDOW SIZE
	HEIGHT = 600 
	WIDTH = 800

	# COLOR
	BLACK = 0, 0, 0
	RED = 255, 0, 0

	# Characters dimensions
	RECT_WIDTH = 60
	RECT_HEIGHT = 80
	x = (WIDTH // 2) - (RECT_HEIGHT//2)
	y = HEIGHT - RECT_HEIGHT - 2


	
	
	# Velocity
	VEL = 5



	is_jump = False
	jump_count = 10


	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	running = True




	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				running = False
				sys.exit()

		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT] and x > 0:
			x -= VEL
		if keys[pygame.K_RIGHT] and x < WIDTH - RECT_WIDTH:
			x += VEL
		if not is_jump:
			if keys[pygame.K_SPACE]:
				is_jump = True
		else:
			if jump_count >= -10:
				neg = 1
				if jump_count < 0:
					neg = -1
				y -= (jump_count**2) * (0.5) * neg
				jump_count -= 1
			else:
				is_jump = False
				jump_count = 10
		screen.fill(BLACK)
		#SURFACE, COLOR,  (POSITION X, POSITION Y, HEIGHT, WIDTH)
		pygame.draw.rect(screen, RED, (x, y, RECT_WIDTH, RECT_HEIGHT))
		pygame.display.update()
			


	


if __name__ == "__main__":
	main()


