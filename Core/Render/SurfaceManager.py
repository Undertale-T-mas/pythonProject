from typing import *

import pygame

import Core.GameStates.GameState
from Core.GameStates.GameState import *
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
                self.buffers[i] = Surface(self.__renderOptions__.screenSize, pygame.SRCALPHA)
            self.screen = Core.GameStates.GameState.set_display(self.__renderOptions__)

    def __init__(self, render_options: RenderOptions):
        self.__renderOptions__ = render_options
        for i in range(BUFFER_COUNT):
            self.buffers.append(Surface(
                (render_options.screenSize.x, render_options.screenSize.y),
                flags=render_options.surfaceFlag)
            )

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
