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
        self.hider = player([325,100], (0, 0, 255), self.display, "hider")

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                exit()

    def checkwin(self):
        winner = "none"
        frames = int((time.time() - self.startTime)*config["screen"]["fps"])
        if frames >= 6000:
            print(f"seaker took to long, hider won after {frames} frames")
            winner = "hider"
        if self.seaker.pos == self.hider.pos:
            frames = int((time.time() - self.startTime)*config["screen"]["fps"])
            print(f"seaker won after {frames} frames")
            winner= "seaker"
        for i in [self.seaker, self.hider]:
            if i.pos[0] < 0 or i.pos[1] < 0 or i.pos[0] > self.width or i.pos[1] > self.height:
                print(f"{i.name} hit wall")
                winner = i.name

        if winner != "none":
            if winner == "seaker":
                self.seaker.wins += 1
                self.hider.losses += 1
            else:
                self.hider.wins += 1
                self.seaker.losses += 1
            for i in [self.seaker, self.hider]:
                i.draw(0)
            self.setup()
