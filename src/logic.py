import pygame
from src.player import player
from config import config
import time


# the game logic that runs everything
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

            #decide moves
            self.seaker.decide(self.hider.pos)
            self.hider.draw((0,0,255))
            # self.hider.decide(self.seaker.pos)
            #check wins
            self.checkwin()

            # update time and display
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
        maxFrames = 6000
        # check wins and count frames untill win condition
        winner = "none"
        frames = int((time.time() - self.startTime)*config["screen"]["fps"])
        self.seaker.score = 1-frames/maxFrames
        self.hider.score = frames/maxFrames
        if frames >= maxFrames:
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
                i.score = 0

        if winner != "none":
            print(self.seaker.score)
            for i in [self.seaker, self.hider]:
                i.draw(0)
            self.setup()
