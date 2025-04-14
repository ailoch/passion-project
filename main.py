import pygame
from globals import *
from util import *
from classes.player import Player
from classes.platform import Platform, PlatformType

# pygame setup
clock = pygame.time.Clock()
running = True
dt = 0

player = Player()

# add platforms to world
worldPlatforms = (Platform((400, 450, 0), (600, 50), PlatformType.GROUND),
                  Platform((943, 363, -20), (500, 50), PlatformType.GROUND))
for plat in worldPlatforms:
    currentPlatforms.append(plat)

while running:
    # poll for events
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_w or event.key==pygame.K_UP:
                events.append(Event.JUMP)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # handle game inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        events.append(Event.MOVELEFT)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        events.append(Event.MOVEDOWN)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        events.append(Event.MOVERIGHT)
    
    # update all entities
    player.tick(events, dt)

    for plat in currentPlatforms:
        plat.render()
    player.render()
    # display framerate
    if dt == 0:
        drawText("1000", (3, 3), font)
    else:
        drawText(str(1/dt)[:2], (3, 0), font)

    # refresh the screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
