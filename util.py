import pygame
from enum import Enum
from globals import *

class Event(Enum):
    E_MOVEUP = 0
    E_MOVELEFT = 1
    E_MOVEDOWN = 2
    E_MOVERIGHT = 3

def getRectPoints(pos, size, rot):
    # get corner offsets from center pos
    upOffset = pygame.Vector2(0, size.y/2)
    downOffset = pygame.Vector2(0, -size.y/2)
    leftOffset = pygame.Vector2(-size.x/2, 0)
    rightOffset = pygame.Vector2(size.x/2, 0)
    # rotate offsets by the rects rotation
    upOffset.rotate_ip(rot)
    downOffset.rotate_ip(rot)
    leftOffset.rotate_ip(rot)
    rightOffset.rotate_ip(rot)
    return (pos+upOffset+leftOffset, pos+upOffset+rightOffset, pos+downOffset+rightOffset, pos+downOffset+leftOffset)

def drawText(text: str, pos: pygame.Vector2, font: pygame.font.Font):
    screen.blit(font.render(text, True, (255, 255, 255)), pos)
