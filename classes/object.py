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
        self.width = 3 # default width for objects

    def _updatePos(self, dt):
        self.pos += self.vel*dt

    def render(self):
        corners = getRectCorners(self.pos, self.size, self.rot, int(self.width*camera.zoom))
        pygame.draw.polygon(screen, self.color, camera.translatePoints(corners), int(self.width*camera.zoom))
