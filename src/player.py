import pygame
class player:
    radius = 5

    def __init__(self, pos):
        self.pos = pos

    def draw(self, display):
        pygame.draw.circle(display, [255,0,0], self.pos, self.radius)
