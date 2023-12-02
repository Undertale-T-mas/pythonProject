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
    picture: Button

    def start(self):
        self.picture=load_image('BackGrounds\\main.jpg')
        self.picture=load_image('BackGrounds\\')
    def update(self, game_args: GameArgs):
        super().update(game_args) # 引擎内部每一帧都必须做的事情

    def draw(self, surface_manager: SurfaceManager,button_manager:SurfaceManager):
        super().draw(surface_manager) # 引擎内部每一帧都必须做的事情
        super().draw(button_manager)
        rec1 = vec2(0, 0)
        rec2 = vec2(540, 400)

        surface_manager.screen.blit(self.picture, rec1) # 把图片画到指定的矩形区域
        button_manager.screen.blit(self.picture, rec2)