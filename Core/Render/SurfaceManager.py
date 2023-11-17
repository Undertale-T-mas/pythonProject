from typing import *

import pygame

from RenderOptions import *
from Core.GameObject import *
from pygame import Vector2 as vec2

BUFFER_COUNT = 3


class SurfaceManager:
    buffers: List[Surface]
    screen: Surface

    __curSize__: vec2
    __renderOptions__: RenderOptions

    def __reset_size__(self):
        if (self.__curSize__ - self.__renderOptions__.screenSize).length_squared() > 0.01:
            self.__curSize__ = self.__renderOptions__.screenSize
            for i in range(BUFFER_COUNT):
                self.buffers[i] = Surface((self.__renderOptions__.screenSize.x, self.__renderOptions__.screenSize.y))
            screen = pygame.display.set_mode(self.__curSize__)

    def __init__(self, render_options: RenderOptions):
        self.__renderOptions__ = render_options
        for i in range(BUFFER_COUNT):
            self.buffers.append(Surface((render_options.screenSize.x, render_options.screenSize.y)))

    def draw_begin(self):
        self.__reset_size__()
        pass

    def draw_insert(self, ent: Entity):
        pass

    def draw_end(self):
        pass
