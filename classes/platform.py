from enum import Enum
from globals import *
from classes.object import Object

class PlatformType(Enum):
    GROUND = {"color": (0, 255, 0), "friction": 12, "accel": 5000}
    LAVA = {"color": (255, 0, 0), "friction": 12, "accel": 5000}
    ICE = {"color": (61, 236, 255), "friction": 2.5, "accel": 2000}

class Platform(Object):
    def __init__(self, pose, size, type):
        super().__init__(pose, size, type.value["color"])
        self.type = type
        self.info = type.value
