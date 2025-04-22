import pygame
from globals import *
from util import *
from classes.object import Object
from classes.platform import PlatformType

class Player(Object):
    def __init__(self):
        super().__init__((0, 0, 0), (100, 100), (144, 0, 255))
        self.prevPos = pygame.Vector2(0, 0)
        self.standingPlats = []
        self.canJump = True
        self.checkpoint = 0
        self.friction = 12
        self.accel = 5000

    def respawn(self):
        self.pos = pygame.Vector2(respawnPoints[self.checkpoint][0])
        self.vel = pygame.Vector2(0, 0)

    # handle player physics
    def tick(self, events, dt):
        if Debug["allowFlight"]:
            if Event.MOVEUP in events:
                self.pos.y -= 800*dt
            if Event.MOVELEFT in events:
                self.pos.x -= 800*dt
            if Event.MOVEDOWN in events:
                self.pos.y += 800*dt
            if Event.MOVERIGHT in events:
                self.pos.x += 800*dt
            return

        # apply gravity
        if self.standingPlats == []:
            self.vel.y += 1900*dt
        else:
            self.vel.y = 0

        # apply friction
        self.vel.x -= self.vel.x*dt*self.friction

        # player movement/jumping
        if Event.JUMP in events and self.canJump:
            self.vel.y = -800
            if self.standingPlats == []:
                self.canJump = False
        if Event.MOVELEFT in events:
            self.vel.x -= self.accel*dt
        if Event.MOVEDOWN in events:
            # nothing for now
            pass
        if Event.MOVERIGHT in events:
            self.vel.x += self.accel*dt

        self._updatePos(dt)

        # handle platform interactions
        collidingPlats = getCollidingPlats(self.pos, self.size, self.rot)
        for plat in collidingPlats:
            # respawn if touching lava
            if plat.type==PlatformType.LAVA:
                if collideRects(self.pos, self.size-(0, 10), self.rot, plat.pos, plat.size, plat.rot):
                    self.respawn()
                    return
                else:
                    continue

            playerCorners = getRectCorners(self.pos, self.size, self.rot)
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
                    self.pos.y += 1
                elif abs(mtv.x) > .5:
                    # hitting wall
                    if self.vel.x*mtv.x < 0:
                        self.vel.x = 0

        # check if on ground
        feetPos = pygame.Vector2(0, self.size.y/2+2).rotate(self.rot)
        feetPos += self.pos
        if Debug["showPlayerFeet"]:
            feetRect = Object((feetPos.x, feetPos.y, self.rot), pygame.Vector2(self.size.x-10, .1), "#ffb0ff")
            feetRect.render()
        self.standingPlats = getCollidingPlats(feetPos, pygame.Vector2(self.size.x-10, .1), self.rot)

        # filter lava platforms
        self.standingPlats = [plat for plat in self.standingPlats if not plat.type==PlatformType.LAVA]

        if self.standingPlats != []:
            self.canJump = True
            # calc friction
            self.friction = float("inf")
            self.accel = float("inf")
            topSpeed = float("inf")
            for plat in self.standingPlats:
                if plat.info["accel"]/plat.info["friction"] < topSpeed:
                    self.friction = plat.info["friction"]
                    self.accel = plat.info["accel"]
                    topSpeed = self.accel/self.friction

        # snap player to platforms
        if self.vel.y > 0:
            for plat in self.standingPlats:
                feetCorners = getRectCorners(feetPos, pygame.Vector2(self.size.x, 1), self.rot)
                platCorners = getRectCorners(plat.pos, plat.size, plat.rot)
                axes = []
                for corners in [feetCorners, platCorners]:
                    for i in range(4):
                        edge = corners[i] - corners[(i+1) % 4]
                        normal = edge.normalize().rotate(90)
                        axes.append(normal)

                mtv = getMtv(feetCorners, platCorners, axes)
                if mtv and mtv.magnitude() > .01:
                    feetPos.y -= mtv.y
                    self.pos.y -= mtv.y

            if self.standingPlats != []:
                feetPos.y += 2
                self.pos.y += 2

        # check for death
        for i in range(0, self.checkpoint+1):
            if pointCrossedLine(self.pos, self.prevPos, respawnPoints[i][1], respawnPoints[i][2]):
                self.respawn()
        # check if reached next area
        if pointCrossedLine(self.pos, self.prevPos, respawnPoints[self.checkpoint][3], respawnPoints[self.checkpoint][4]):
            if self.checkpoint < len(respawnPoints)-1:
                self.checkpoint += 1

        self.prevPos = pygame.Vector2(self.pos)
