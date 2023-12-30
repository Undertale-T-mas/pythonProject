import sys

import pygame

import Game.TestScene
from Core.GameStates import GameState
from Core.GameStates.Scene import Scene
from Core.Render.RenderOptions import *
from Game.Map.Framework.WorldManager import __quitSave__
from Game.Scenes.Start import *
from Core.GameStates.KeyIdentity import KeyIdentity as ki
from Game.TestScene import *
from pygame import Vector2 as vec2
from Game.Map.Framework.WorldManager import *
import Resources.ResourceLib
from Resources.ResourceLib import *

# pygame setup

pygame.init()
pygame.display.set_caption('Machine Rebel')
pygame.mixer.pre_init(44100, 16, 2, 4096)
Resources.ResourceLib.Sounds.initialize()
Resources.ResourceLib.Fonts.initialize()
render_options = RenderOptions()
clock = pygame.time.Clock()
pygame.key.stop_text_input()
running = True
dt = 0

GameState.initialize(render_options)
# WorldManager.respawn()
GameState.change_scene(Start())

flipped = False

speed = 1e0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    GamingGL.begin()
    if GameState.update(dt):
        break
    GameState.render()
    GamingGL.end()

    if GameState.key_hold(ki.speed_0):
        speed = 0.01
    if GameState.key_hold(ki.speed_1):
        speed = 0.025
    if GameState.key_hold(ki.speed_2):
        speed = 0.05
    if GameState.key_hold(ki.speed_3):
        speed = 0.1
    if GameState.key_hold(ki.speed_4):
        speed = 0.25

    if GameState.key_hold(ki.speed_5):
        speed = 0.5
    if GameState.key_hold(ki.speed_6):
        speed = 0.7
    if GameState.key_hold(ki.speed_7):
        speed = 1
        # flip() the display to put your work on screen
    if not flipped:
        flipped = True
        pygame.display.flip()
    else:
        pygame.display.flip()

    # limits FPS to 144
    # dt is delta time in seconds since last frame, used for frame rate
    # independent physics.
    dt = min(clock.tick(144) / 1000, 0.04) * speed

__quitSave__()
clock.tick(10)
pygame.quit()
sys.exit()
