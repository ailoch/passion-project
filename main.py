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
worldPlatforms = (Platform((-240, 90, 0), (600, 50), PlatformType.GROUND),
                  Platform((303, 3, -20), (500, 50), PlatformType.GROUND),
                  Platform((0, 350, 2), (1300, 50), PlatformType.GROUND),
                  Platform((1000, 150, 0), (250, 50), PlatformType.GROUND),
                  Platform((-750, 0, 0), (50, 1000), PlatformType.GROUND),
                  Platform((-550, -200, 5), (150, 50), PlatformType.GROUND),
                  Platform((1250, 150, 0), (250, 50), PlatformType.LAVA),
                  Platform((1750, 150, 0), (750, 50), PlatformType.ICE),
                  Platform((2375, 150, 0), (500, 50), PlatformType.GROUND))
for plat in worldPlatforms:
    currentPlatforms.append(plat)

#           respawn  trigger                  area complete
respawn = (((0, 0), (-2500, 700, 2000, 700), (830, -1000, 830, 150)),
           ((1000, 70), (830, 700, 4000, 700), (2000, -1000, 2000, 1000)))
for point in respawn:
    respawnPoints.append((pygame.Vector2(point[0]), pygame.Vector2(point[1][0:2]), pygame.Vector2(point[1][2:4]), pygame.Vector2(point[2][0:2]), pygame.Vector2(point[2][2:4])))

while running:
    # poll for events
    events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if user closed the window
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_w or event.key==pygame.K_UP or event.key==pygame.K_SPACE:
                events.append(Event.JUMP)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if Debug["clickForPos"]:
                clickPos = event.pos
                clickPos -= pygame.Vector2(screen.get_width()/2, screen.get_height()/2)
                clickPos /= camera.zoom
                clickPos += camera.pos
                print(str(clickPos.x) + ", " + str(clickPos.y))

    # handle game inputs
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
        events.append(Event.MOVEUP)
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

    # show checkpoints
    if Debug["showRespawnPoints"]:
        for i in range(len(respawnPoints)):
            checkpointColors = (((127, 100, 100), (100, 127, 100)),
                                ((255, 200, 200), (200, 255, 200)),
                                ((191, 150, 150), (150, 191, 150)))
            point = respawnPoints[i]
            colors = checkpointColors[sgn(i-player.checkpoint) + 1]
            pygame.draw.circle(screen, colors[0], camera.translatePoint(point[0]), 7*camera.zoom)
            pygame.draw.line(screen, colors[0], camera.translatePoint(point[1]), camera.translatePoint(point[2]), int(4*camera.zoom))
            pygame.draw.line(screen, colors[1], camera.translatePoint(point[3]), camera.translatePoint(point[4]), int(4*camera.zoom))

    # display framerate
    if dt == 0:
        drawText("1000", (3, 3), font)
    else:
        drawText(str(1/dt)[:2], (3, 0), font)

    # refresh the screen
    pygame.display.flip()

    # delay so the framerate remains at 60
    dt = clock.tick(60)/1000

pygame.quit()
