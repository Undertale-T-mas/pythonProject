import Game.Map.Begin.TestMap
from Core.MathUtil import *
import random

import pygame.draw_py
from pygame import *
import pygame
from Game.Characters.Humans.Player import *


class Start(Scene):
    time_tot = 0
    picture_background: Surface
    picture_startbutton: Surface

    def start(self):
        self.picture_background=load_image('BackGrounds\\main.jpg')
        self.picture_startbutton=load_image('BackGrounds\\start game.png')
    def update(self, game_args: GameArgs):
        super().update(game_args) # 引擎内部每一帧都必须做的事情

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager) # 引擎内部每一帧都必须做的事情
        rec1 = vec2(0, 0)
        rec2 = vec2(10, 100)

        surface_manager.screen.blit(self.picture_background, rec1) # 把图片画到指定的矩形区域
        surface_manager.screen.blit(self.picture_startbutton, rec2)