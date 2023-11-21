import math
import random

import pygame.draw_py

from Core.GameArgs import GameArgs, RenderArgs
from Core.GameObject import Entity
from Core.GameStates import GameStates
from Core.GameStates.Scene import Scene
from pygame import Vector2 as vec2

from Core.Render.SurfaceManager import SurfaceManager


class TestObject(Entity):
    y = 0
    appear_time = 0

    def __init__(self):
        self.y = random.randint(100, 700)

    def update(self, args: GameArgs):
        self.appear_time += args.elapsedSec
        self.centre = vec2(math.sin(self.appear_time) * 420 + 640, self.y)
        if self.appear_time > 5: self.dispose()

    def draw(self, render_args: RenderArgs):
        pygame.draw.circle(render_args.target_surface, [255, 255, 255, 255], self.centre, 100.0)


class TestScene(Scene):
    time_tot = 0

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.time_tot += game_args.elapsedSec
        if self.time_tot > 1:
            self.time_tot -= 1
            GameStates.instance_create(TestObject())

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager)
        rect = pygame.rect.Rect(0, 0, self.__render_options__.screenSize.x, self.__render_options__.screenSize.y)
        surface_manager.screen.blit(
            surface_manager.get_surface('default'),
            dest=rect,
            area=rect,
        )
