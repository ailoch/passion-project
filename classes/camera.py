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
        windowCenter = pygame.Vector2(globals.screen.get_width()/2, globals.screen.get_height()/2)
        translatedPoint = point-self.pos
        translatedPoint *= self.zoom
        return translatedPoint + windowCenter

    def follow(self, pos, zoom, dt):
        error = self.pos-pos
        error -= error*dt*12
        self.pos = pos+error
        self.zoom = zoom
