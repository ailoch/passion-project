import pygame
from classes.camera import Camera

# debug mode
Debug = {"allowFlight": False,
         "clickForPos": False,
         "levelEditor": False,
         "showPlayerFeet": False,
         "showRespawnPoints": False
         }

# pygame setup
pygame.init()
screenSize = pygame.Vector2(1280, 720)
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Passion project")
font = pygame.font.SysFont("Arial", 18)

# platform list
currentPlatforms = []

# respawn point list
respawnPoints = []

# create the camera
camera = Camera()
