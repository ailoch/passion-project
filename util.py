import pygame
from enum import Enum
from globals import *

class Event(Enum):
    JUMP = 0
    MOVEUP = 1
    MOVELEFT = 2
    MOVEDOWN = 3
    MOVERIGHT = 4

# get the sign of a number
def sgn(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0

def signedDist(pos, lPos, lVector):
    return lVector.x * (lPos.y-pos.y) - lVector.y * (lPos.x-pos.x)

def pointCrossedLine(curr, prev, l1, l2):
    lVector = pygame.Vector2(l2-l1).normalize()
    currSide = sgn(signedDist(curr, l1, lVector))
    prevSide = sgn(signedDist(prev, l1, lVector))
    if currSide == prevSide: # if point did not cross line
        return False
    # check if point crossed between endpoints of line
    lVector.rotate_ip(90)
    side1 = sgn(signedDist(prev, l1, lVector))
    side2 = sgn(signedDist(prev, l2, lVector))
    return side1 != side2

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
    return max1>=min2 and max2>=min1

def collideRects(pos1, size1, rot1, pos2, size2, rot2):
    rect1 = getRectCorners(pos1, size1, rot1)
    rect2 = getRectCorners(pos2, size2, rot2)

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

        if (max1<min2 or max2<min1): # no collision
            return None

        overlap = min(max1, max2)-max(min1, min2)
        if overlap < smallestOverlap:
            smallestOverlap = overlap
            smallestAxis = axis

    dir = poly2[0]-poly1[0]
    if dir.dot(smallestAxis) < 0:
        smallestAxis = -smallestAxis

    return smallestAxis * smallestOverlap

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

def drawText(text, pos, font):
    screen.blit(font.render(text, True, (255, 255, 255)), pos)
