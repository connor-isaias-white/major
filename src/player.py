import pygame
from config import config
import random

class player:
    radius = 5

    def __init__(self, pos, colour, display, name):
        self.pos = pos
        self.colour = colour
        self.display = display
        self.name = name

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

    def see(self, enemyPos):
        upEye = self.pos[1]
        downEye = config["screen"]["height"] -self.pos[1]
        leftEye = self.pos[0]
        rightEye = config["screen"]["width"] -self.pos[0]
        enemyDist = ((self.pos[0] - enemyPos[0])**2 + (self.pos[1] - enemyPos[1])**2)**(1/2)
        # print(f"{self.name}: up: {upEye}, down: {downEye}, left: {leftEye}, right: {rightEye}, enemyPos: {enemyPos}, ownPos: {self.pos}, enemyDist: {enemyDist}")

    def decide(self, enemyPos):
        self.see(enemyPos)
        directions = ["up", "down", "left", "right"]
        choice = random.randint(0, 3)
        self.move(directions[choice])
