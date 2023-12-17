from typing import *

import pygame

from Core.Render.RenderOptions import *
from Core.GameObject import *
from pygame import Vector2 as vec2

BUFFER_COUNT = 6


class SurfaceManager:
    buffers: List[Surface] = []
    screen: Surface

    __ent_buffer__: List[Entity] = []
    __curSize__: vec2 = vec2(0, 0)
    __renderOptions__: RenderOptions
    __ent_dict__: Dict[str, int] = dict()
    __ent_exist__: Set[int] = set()

    @staticmethod
    def set_display(render_options: RenderOptions) -> Surface:
        return pygame.display.set_mode(render_options.screenSize, render_options.surfaceFlag)

    def exist_surface(self, _name: str) -> bool:
        if _name not in self.__ent_dict__:
            return False
        val = self.__ent_dict__[_name]
        return val in self.__ent_exist__

    def get_surface(self, _name: str):
        if _name not in self.__ent_dict__:
            self.__ent_dict__[_name] = len(self.__ent_dict__)
        return self.buffers[self.__ent_dict__[_name]]

    def __reset_size__(self):
        if (self.__curSize__ - self.__renderOptions__.screenSize).length_squared() > 0.01:
            self.__curSize__ = self.__renderOptions__.screenSize
            for i in range(BUFFER_COUNT):
                self.buffers[i] = Surface(self.__renderOptions__.screenSize, self.__renderOptions__.surfaceFlag)

            if self.__renderOptions__.extraBuffer:
                self.screen = Surface(self.__renderOptions__.screenSize, self.__renderOptions__.surfaceFlag)
                self.display = SurfaceManager.set_display(self.__renderOptions__)
            else:
                self.screen = SurfaceManager.set_display(self.__renderOptions__)
                self.display = self.screen

    def __init__(self, render_options: RenderOptions):
        self.__renderOptions__ = render_options
        for i in range(BUFFER_COUNT):
            self.buffers.append(Surface(
                (render_options.screenSize.x, render_options.screenSize.y),
                flags=render_options.surfaceFlag)
            )
        self.__reset_size__()

    def draw_begin(self):
        self.__reset_size__()
        self.__ent_buffer__.clear()
        self.screen.fill([0, 0, 0])
        self.__ent_exist__.clear()

    def draw_insert(self, ent: Entity):
        if ent.surfaceName not in self.__ent_dict__:
            self.__ent_dict__[ent.surfaceName] = len(self.__ent_dict__)
        self.__ent_buffer__.append(ent)

    def draw_end(self, render_args: RenderArgs):
        render_args.settings = self.__renderOptions__
        for ent in self.__ent_buffer__:
            idx = self.__ent_dict__[ent.surfaceName]
            if idx not in self.__ent_exist__:
                self.buffers[idx].fill([0, 0, 0, 0])

            self.__ent_exist__.add(idx)
            render_args.target_surface = self.buffers[idx]
            ent.draw(render_args)
