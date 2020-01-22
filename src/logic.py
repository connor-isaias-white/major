import pygame
from src.player import player
from config import config

class logic:
    def __init__(self, display):
        self.display = display
        self.running = True

    def loop(self):
        self.setup()
        clock = pygame.time.Clock()
        while self.running:
            self.events()
            pygame.display.update()
            clock.tick(config['screen']['fps'])

    def setup(self):
        seaker = player([50,50])
        seaker.draw(self.display)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                exit()
