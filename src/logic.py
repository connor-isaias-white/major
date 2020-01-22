import pygame
from src.player import player
from config import config
import time

class logic:
    def __init__(self, display):
        self.display = display
        self.running = True
        self.width = config['screen']['width']
        self.height = config['screen']['height']

    def loop(self):
        self.setup()
        clock = pygame.time.Clock()
        while self.running:
            self.events()

            self.seaker.decide(self.hider.pos)
            self.hider.decide(self.seaker.pos)
            self.checkwin()

            pygame.display.update()
            clock.tick(config['screen']['fps'])

    def setup(self):
        self.startTime = time.time()
        self.seaker = player([175,100], (255, 0, 0), self.display, "seaker")
        self.hider = player([325,100], (0, 255, 0), self.display, "hider")

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                exit()

    def checkwin(self):
        if self.seaker.pos == self.hider.pos:
            frames = int((time.time() - self.startTime)*config["screen"]["fps"])
            print(f"seaker won after {frames} frames")
        for i in [self.seaker, self.hider]:
            if i.pos[0] < 0 or i.pos[1] < 0 or i.pos[0] > self.width or i.pos[1] > self.height:
                print(f"{i.name} hit wall")
