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
        if event.type == pygame.QUIT: # if user closed the window
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_w or event.key==pygame.K_UP:
                events.append(Event.JUMP)

    # handle game inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        events.append(Event.MOVELEFT)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        events.append(Event.MOVEDOWN)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        events.append(Event.MOVERIGHT)

    # clear the screen so a new frame can be drawn
    screen.fill("black")

    # update the camera
    camera.follow(player.pos, .8, dt)

    # update all entities
    player.tick(events, dt)

    # render entities
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

    # delay so the framerate remains at 60
    dt = clock.tick(60) / 1000

pygame.quit()
