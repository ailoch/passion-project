import pygame
from globals import *
from util import *

class Object:
    def __init__(self, pose, size, color):
        self.pos = pygame.Vector2(pose[0], pose[1])
        self.size = pygame.Vector2(size)
        self.rot = pose[2]
        self.vel = pygame.Vector2(0, 0)
        self.color = color
        self.width = 3

    def _updatePos(self, dt):
        self.pos += self.vel*dt

    def render(self):
        pygame.draw.polygon(screen, self.color, getRectCorners(self.pos, self.size, self.rot), self.width)
