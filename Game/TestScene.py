import Game.Map.Begin.TestMap
from Core.MathUtil import *
import random

import pygame.draw_py

from Game.Characters.Humans.Player import *


class TestScene(FightScene):
    time_tot = 0

    def start(self):
        self.set_tiles(Game.Map.Begin.TestMap.MapTEST0())
        GameStates.instance_create(Player())

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.time_tot += game_args.elapsedSec
        if self.time_tot > 1:
            self.time_tot -= 1

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager)
        rec = pygame.rect.Rect(0, 0, self.__render_options__.screenSize.x, self.__render_options__.screenSize.y)
        surface_manager.screen.blit(
            surface_manager.get_surface('bg'),
            dest=rec,
            area=rec,
        )
        surface_manager.screen.blit(
            surface_manager.get_surface('default'),
            dest=rec,
            area=rec,
        )
