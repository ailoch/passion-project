import pygame
import globals

class Camera:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.zoom = 1

    def translatePoints(self, points):
        translatedPoints = []
        for point in points:
            translatedPoints.append(self.translatePoint(point))
        return translatedPoints

    def translatePoint(self, point):
        windowCenter = globals.screenSize/2
        translatedPoint = point-self.pos
        translatedPoint *= self.zoom
        return translatedPoint + windowCenter

    def reverseTranslate(self, point):
        translatedPoint = point - globals.screenSize/2
        translatedPoint /= self.zoom
        return translatedPoint+self.pos

    def follow(self, pos, zoom, dt):
        error = self.pos-pos
        error -= error*dt*12
        self.pos = pos+error
        self.zoom = zoom
