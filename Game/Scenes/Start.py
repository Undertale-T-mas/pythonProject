import Game.Map.Begin.TestMap
from Core.MathUtil import *
import random

import pygame.draw_py
from pygame import *
import pygame
from Game.Characters.Humans.Player import *


class Start(Scene):
    time_tot = 0
    picture: Surface

    def start(self):
        self.picture=load_image('BackGrounds\\main.jpg')

    def update(self, game_args: GameArgs):
        super().update(game_args) # 引擎内部每一帧都必须做的事情

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager) # 引擎内部每一帧都必须做的事情
        rec = vec2(0, 0)

        surface_manager.screen.blit(self.picture, rec) # 把图片画到指定的矩形区域
