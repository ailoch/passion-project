import pygame
from globals import *
from util import *
from classes.player import Player

# pygame setup
clock = pygame.time.Clock()
running = True
dt = 0

player = Player()

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # handle game inputs
    events = []
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        events.append(Event.E_MOVEUP)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        events.append(Event.E_MOVELEFT)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        events.append(Event.E_MOVEDOWN)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        events.append(Event.E_MOVERIGHT)
    
    # update all entities
    player.tick(events, dt)

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
