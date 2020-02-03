import pygame
from config import config
import random
import math

class player:
    radius = 5

    def __init__(self, pos, colour, display, name):
        self.pos = pos
        self.colour = colour
        self.display = display
        self.name = name
        self.score = 0

    def draw(self, colour):
        pygame.draw.circle(self.display, colour, self.pos, self.radius)

    def move(self, direction):
        self.draw(0)

        if direction == "up":
            self.pos[1] -= 1
        elif direction == "down":
            self.pos[1] += 1
        elif direction == "left":
            self.pos[0] -= 1
        elif direction == "right":
            self.pos[0] += 1
        else:
            print("not a direction")

        self.draw(self.colour)

    def see(self):
        # upEye = self.pos[1]
        # downEye = config["screen"]["height"] -self.pos[1]

        #calculate bearing
        if (self.enemyPos[0]-self.pos[0]) != 0:
            self.bearing = math.atan((self.enemyPos[1]-self.pos[1])/(self.enemyPos[0]-self.pos[0]))
        else:
            self.bearing = 90

        if (self.enemyPos[1]-self.pos[1]) < 0 and (self.enemyPos[0]-self.pos[0]) <0:
            self.bearing = 180 -self.bearing
        elif (self.enemyPos[1]-self.pos[1]) < 0 :
            self.bearing = 360 -self.bearing
        elif (self.enemyPos[0]-self.pos[0]) < 0:
            self.bearing = self.bearing + 180

        self.leftEye = self.pos[0]
        self.rightEye = config["screen"]["width"] -self.pos[0]
        self.enemyDist = abs(self.pos[0] - self.enemyPos[0])
        # print(f"{self.name}: left: {leftEye}, right: {rightEye}, enemyPos: {enemyPos[0]}, ownPos: {self.pos[0]}, enemyDist: {enemyDist}, self.bearing: {self.bearing}")

    def decide(self, enemyPos):
        self.enemyPos = enemyPos
        self.see()
        directions = ["left", "right"]
        choice = random.randint(0, 1)
        self.move(directions[choice])
