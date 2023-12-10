import pygame

import Game.TestScene
import Resources.ResourceLib
from Core.GameStates import GameState
from Core.GameStates.Scene import Scene
from Core.Render.RenderOptions import *
from Game.Scenes.Start import *
from Game.TestScene import *
from pygame import Vector2 as vec2
from Game.Map.Framework.WorldManager import *

# pygame setup
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
Resources.ResourceLib.Sounds.initialize()
render_options = RenderOptions()
clock = pygame.time.Clock()
pygame.key.stop_text_input()
running = True
dt = 0

GameState.initialize(render_options)
WorldManager.respawn()
# GameStates.change_scene(Start())

flipped = False

speed = 1

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    GameState.update(dt)
    GameState.render()

    # flip() the display to put your work on screen
    if not flipped:
        flipped = True
        pygame.display.flip()
    else:
        pygame.display.flip()

    # limits FPS to 125
    # dt is delta time in seconds since last frame, used for frame rate
    # independent physics.
    dt = min(clock.tick(125) / 1000, 0.1) * speed

pygame.quit()