#!/anaconda3/bin/python3
import pygame





SCREEN_W = 800
SCREEN_H = 600
POS_X = SCREEN_W // 2
POS_Y = SCREEN_H // 2
WIDTH = 50
HEIGHT = 70



BLACK = (0, 0, 0)


def main():
	

	
	pygame.init()

	pygame.display.set_caption("First Python Game")
	screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

	screen.fill((0,0,0))
	
	running = True

	while running:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
	screen.fill(BLACK)	
	pygame.draw.rect(screen, (255, 0, 0), (POS_X, POS_Y, WIDTH, HEIGHT))
	
	pygame.display.flip()

if __name__ == "__main__":
	main()


