import pygame
from enum import Enum
from globals import *

class Event(Enum):
    JUMP = 0
    MOVELEFT = 1
    MOVEDOWN = 2
    MOVERIGHT = 3

def getRectCorners(pos, size, rot, width=0):
    # get corner offsets from center pos
    upOffset = pygame.Vector2(0, size.y/2 - width)
    downOffset = pygame.Vector2(0, -size.y/2 + width)
    leftOffset = pygame.Vector2(-size.x/2 + width, 0)
    rightOffset = pygame.Vector2(size.x/2 - width, 0)
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

def projectPoly(points, axis):
    dots = [point.dot(axis) for point in points]
    return min(dots), max(dots)

def overlapOnAxis(poly1, poly2, axis):
    min1, max1 = projectPoly(poly1, axis)
    min2, max2 = projectPoly(poly2, axis)
    return max1>= min2 and max2>=min1

def collideRects(pos1, size1, rot1, pos2, size2, rot2):
    rect1 = getRectCorners(pos1, size1, rot1)
    rect2 = getRectCorners(pos2, size2, rot2)

    #edges = rect1+rect2
    axes = []

    for i in range(4):
        edge1 = rect1[i] - rect1[(i+1) % 4]
        edge2 = rect2[i] - rect2[(i+1) % 4]
        axes.append(edge1.normalize().rotate(90))
        axes.append(edge2.normalize().rotate(90))

    for axis in axes:
        if not overlapOnAxis(rect1, rect2, axis):
            return False
    return True

def getCollidingPlats(pos, size, rot):
    collidingPlats = []
    for plat in currentPlatforms:
        if collideRects(pos, size, rot, plat.pos, plat.size, plat.rot):
            collidingPlats.append(plat)
    return collidingPlats

def getMtv(poly1, poly2, axes):
    smallestOverlap = float("inf")
    smallestAxis = None

    for axis in axes:
        min1, max1 = projectPoly(poly1, axis)
        min2, max2 = projectPoly(poly2, axis)

        if max1 < min2 or max2 < min1:  # no collision
            return None
        
        overlap = min(max1, max2)-max(min1, min2)
        if overlap < smallestOverlap:
            smallestOverlap = overlap
            smallestAxis = axis
    
    dir = poly2[0]-poly1[0]
    if dir.dot(smallestAxis) < 0:
        smallestAxis = -smallestAxis
    
    return smallestAxis * smallestOverlap

def drawText(text, pos, font):
    screen.blit(font.render(text, True, (255, 255, 255)), pos)
    