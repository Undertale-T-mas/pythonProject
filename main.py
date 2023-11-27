import pygame

import Game.TestScene
from Core.GameStates import GameStates
from Core.GameStates.Scene import Scene
from Core.Render.RenderOptions import *

from pygame import Vector2 as vec2

# pygame setup
pygame.init()
render_options = RenderOptions()
clock = pygame.time.Clock()
pygame.key.stop_text_input()
running = True
dt = 0

GameStates.initialize(render_options)
GameStates.change_scene(Game.TestScene.TestScene())

flipped = False

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    GameStates.update(dt)
    GameStates.render()

    # flip() the display to put your work on screen
    if not flipped:
        flipped = True
        pygame.display.flip()
    else:
        pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for frame rate
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()