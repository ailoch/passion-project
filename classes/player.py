import pygame
from enum import Enum
from globals import *
from util import *
from classes.object import Object

class Player(Object):
    def __init__(self):
        super().__init__((screen.get_width()/2, screen.get_height()/2, 0), (80, 80), (255, 0, 0))

    # handle player physics
    def tick(self, events, dt):
        if Event.E_MOVEUP in events:
            self.pos.y -= 300*dt
        if Event.E_MOVELEFT in events:
            self.pos.x -= 300*dt
        if Event.E_MOVEDOWN in events:
            self.pos.y += 300*dt
        if Event.E_MOVERIGHT in events:
            self.pos.x += 300*dt
