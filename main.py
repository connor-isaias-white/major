import pygame
from src.logic import logic
from config import config

def main():
    pygame.init()
    display = pygame.display.set_mode((config['screen']['width'], config['screen']['height']))
    pygame.display.set_caption(config['screen']['caption'])

    Logic = logic(display)
    Logic.loop()

if __name__ == "__main__":
	main()
	pygame.quit()
	quit()
