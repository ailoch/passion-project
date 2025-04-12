import pygame
from enum import Enum
from globals import *

class Event(Enum):
    E_MOVEUP = 0
    E_MOVELEFT = 1
    E_MOVEDOWN = 2
    E_MOVERIGHT = 3

def getRectPoints(pos, size, rot):
    rightOffset = pygame.Vector2(-size.x, 0)
    rightOffset.rotate_ip(rot)
    downOffset = pygame.Vector2(0, -size.y)
    downOffset.rotate_ip(rot)
    return (pos, pos+rightOffset, pos+rightOffset+downOffset, pos+downOffset)

def drawText(text: str, pos: pygame.Vector2, font: pygame.font.Font):
    screen.blit(font.render(text, True, (255, 255, 255)), pos)
