from globals import *
from util import *
from classes.object import Object

class Player(Object):
    def __init__(self):
        super().__init__((0, 0, 0), (100, 100), (144, 0, 255))
        self.prevPos = pygame.Vector2(0, 0)
        self.onGround = True
        self.canJump = True
        self.checkpoint = 0

    # handle player physics
    def tick(self, events, dt):
        # gravity
        if (self.onGround):
            self.vel.y = 0
        else:
            self.vel.y += 1900*dt

        # apply friction
        self.vel.x -= self.vel.x*dt*12

        # player movement/jumping
        if Event.JUMP in events and self.canJump:
            self.vel.y = -800
            if not self.onGround:
                self.canJump = False
        if Event.MOVELEFT in events:
            self.vel.x -= 5000*dt
        if Event.MOVEDOWN in events:
            # nothing for now
            pass
        if Event.MOVERIGHT in events:
            self.vel.x += 5000*dt

        self._updatePos(dt)

        self.onGround = False
        # handle platform interactions
        collidingPlats = getCollidingPlats(self.pos, self.size, self.rot)
        playerCorners = getRectCorners(self.pos, self.size, self.rot)
        for plat in collidingPlats:
            platCorners = getRectCorners(plat.pos, plat.size, plat.rot)
            axes = []
            for corners in [playerCorners, platCorners]:
                for i in range(4):
                    edge = corners[i] - corners[(i+1) % 4]
                    normal = edge.normalize().rotate(90)
                    axes.append(normal)
            
            mtv = getMtv(playerCorners, platCorners, axes)
            if mtv and mtv.magnitude() > .01:
                # push player out
                self.pos -= mtv
                # cancel velocity
                mtv.normalize_ip()
                if mtv.y < -.5:
                    # hitting ceiling
                    if self.vel.y < 0:
                        self.vel.y = 0
                elif mtv.y > .5:
                    # hitting floor
                    if self.vel.y > 0:
                        self.vel.y = 0
                    self.onGround = True
                    self.canJump = True
                    self.pos.y += 1
                elif abs(mtv.x) > .5:
                    # hitting wall
                    if self.vel.x*mtv.x < 0:
                        self.vel.x = 0

        # check for death
        if pointCrossedLine(self.pos, self.prevPos, respawnPoints[self.checkpoint][1], respawnPoints[self.checkpoint][2]):
            # respawn
            self.pos = pygame.Vector2(respawnPoints[self.checkpoint][0])
            self.vel = pygame.Vector2(0, 0)

        self.prevPos = pygame.Vector2(self.pos)
