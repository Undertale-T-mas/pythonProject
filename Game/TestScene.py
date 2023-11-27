from Core.MathUtil import *
import random

import pygame.draw_py

from Game.Characters.Humans.Player import *


class TestObject(Entity):
    y = 0
    appear_time = 0

    def __init__(self):
        self.y = random.randint(100, 700)

    def update(self, args: GameArgs):
        self.appear_time += args.elapsedSec
        self.centre = vec2(Math.sin(self.appear_time) * 420 + 640, self.y)
        if self.appear_time > 5:
            self.dispose()

    def draw(self, render_args: RenderArgs):
        pygame.draw.circle(render_args.target_surface, [255, 255, 255, 255], self.centre, 100.0)


class TestScene(Scene):
    time_tot = 0

    def start(self):
        GameStates.instance_create(Player())

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.time_tot += game_args.elapsedSec
        if self.time_tot > 1:
            self.time_tot -= 1
            GameStates.instance_create(TestObject())

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager)
        rec = pygame.rect.Rect(0, 0, self.__render_options__.screenSize.x, self.__render_options__.screenSize.y)
        surface_manager.screen.blit(
            surface_manager.get_surface('default'),
            dest=rec,
            area=rec,
        )
