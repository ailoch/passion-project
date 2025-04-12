import pygame
from globals import *
from util import *

class Object:
    def __init__(self, pose, size, color):
        self.pos = pygame.Vector2(pose[0], pose[1])
        self.size = pygame.Vector2(size)
        self.rot = pose[2]
        self.color = color
        self.width = 3

    def render(self):
        pygame.draw.polygon(screen, self.color, getRectPoints(self.pos, self.size, self.rot), self.width)
