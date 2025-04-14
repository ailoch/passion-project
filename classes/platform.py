from enum import Enum
from globals import *
from classes.object import Object

class PlatformType(Enum):
    GROUND = 0

platformColors = {PlatformType.GROUND: (0, 255, 0)}

class Platform(Object):
    def __init__(self, pose, size, type):
        super().__init__(pose, size, platformColors[type])
        self.type = type
