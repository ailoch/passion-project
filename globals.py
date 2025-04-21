import pygame
from classes.camera import Camera

# debug mode
Debug = {"allowFlight": True,
         "clickForPos": True,
         "showPlayerFeet": False,
         "showRespawnPoints": True
         }

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
font = pygame.font.SysFont("Arial", 18)

# platform list
currentPlatforms = []

# respawn point list
respawnPoints = []

# create the camera
camera = Camera()
