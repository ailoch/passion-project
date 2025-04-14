import pygame
from enum import Enum
from globals import *

class Event(Enum):
    JUMP = 0
    MOVELEFT = 1
    MOVEDOWN = 2
    MOVERIGHT = 3

def getRectCorners(pos, size, rot):
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

def pointInBox(point, rectPos, rectSize, rectRot):
    translatedPoint = point-rectPos
    translatedPoint.rotate_ip(-rectRot)

    halfRectSize = rectSize/2
    return (-halfRectSize.x<=translatedPoint.x<=halfRectSize.x) and (-halfRectSize.y<=translatedPoint.y<=halfRectSize.y)

def getTopY(x, rectPos, rectSize, rectRot):
    corners = getRectCorners(rectPos, rectSize,rectRot)
    edges = [(corners[0], corners[1]),
             (corners[1], corners[2]),
             (corners[2], corners[3]),
             (corners[3], corners[0])]
    
    yCandidates = []
    for a, b in edges:
        if (a.x<=x<=b.x) or (b.x<=x<=a.x):
            t = (x-a.x) / (b.x-a.x) if b.x!=a.x else 0
            y = a.y + t * (b.y-a.y)
            yCandidates.append(y)
    
    return min(yCandidates) if yCandidates else None

def drawText(text: str, pos: pygame.Vector2, font: pygame.font.Font):
    screen.blit(font.render(text, True, (255, 255, 255)), pos)
    