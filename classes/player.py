from globals import *
from util import *
from classes.object import Object

class Player(Object):
    def __init__(self):
        super().__init__((screen.get_width()/2, screen.get_height()/2, 0), (100, 100), (255, 0, 0))
        self.onGround = True
        self.standingPlat = None

    # handle player physics
    def tick(self, events, dt):
        # handle platform interactions
        self.onGround = False
        standingPlats = []
        bottom = self.pos + (0, self.size.y/2)
        for plat in currentPlatforms:
            if pointInBox(bottom, plat.pos, plat.size, plat.rot):
                standingPlats.append((getTopY(bottom.x, plat.pos, plat.size, plat.rot), plat))

        if standingPlats == []:
            self.onGround = False
        else:
            self.onGround = True
            minY = standingPlats[0][0]
            self.standingPlat = standingPlats[0]
            for i in range(0, len(standingPlats)):
                if standingPlats[i][0] < minY:
                    minY = standingPlats[i][0]
                    self.standingPlat = standingPlats[i]

        # move out of floors
        if (self.onGround):
            self.pos.y = self.standingPlat[0] - self.size.y/2

        # gravity
        if (self.onGround):
            self.vel.y = 0
        else:
            self.vel.y += 1900*dt

        # apply friction
        self.vel.x -= self.vel.x*dt*12

        # player movement/jumping
        if Event.JUMP in events:
            self.vel.y = -800
        if Event.MOVELEFT in events:
            self.vel.x -= 5000*dt
        if Event.MOVEDOWN in events:
            # nothing for now
            pass
        if Event.MOVERIGHT in events:
            self.vel.x += 5000*dt

        self._updatePos(dt)
