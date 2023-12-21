from typing import *

import pygame

from Core.Entity import Entity
from Core.GameArgs import RenderArgs
from Core.GamingGL.GLBase import RenderTarget
from Core.Render.RenderOptions import *
from Core.GameObject import *
from Core.MathUtil import ColorV4 as cv4
from pygame import Vector2 as vec2, Surface

BUFFER_COUNT = 8


class SurfaceManager:
    buffers: List[RenderTarget | None] = []
    screen: RenderTarget

    __ent_buffer__: List[Entity] = []
    __curSize__: vec2 = vec2(0, 0)
    __renderOptions__: RenderOptions
    __ent_dict__: Dict[str, int] = dict()
    __ent_exist__: Set[int] = set()

    __not_visibles__: Set[str]

    def set_visible(self, sur: str, state: bool):
        if state:
            if sur in self.__not_visibles__:
                self.__not_visibles__.remove(sur)

        else:
            if sur not in self.__not_visibles__:
                self.__not_visibles__.add(sur)

    @staticmethod
    def set_display(render_options: RenderOptions) -> RenderTarget:
        pygame.display.set_mode(render_options.screenSize, render_options.renderTargetFlag)
        return RenderTarget(render_options.screenSize.x, render_options.screenSize.y, True)

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

            if self.__renderOptions__.extraBuffer:
                self.display = SurfaceManager.set_display(self.__renderOptions__)
                self.screen = RenderTarget(self.__curSize__.x, self.__curSize__.y)
            else:
                self.screen = SurfaceManager.set_display(self.__renderOptions__)
                self.display = self.screen

            for i in range(BUFFER_COUNT):
                self.buffers[i] = RenderTarget(self.__renderOptions__.screenSize.x, self.__renderOptions__.screenSize.y)

    def __init__(self, render_options: RenderOptions):
        self.__renderOptions__ = render_options
        for i in range(BUFFER_COUNT):
            self.buffers.append(None)
        self.__reset_size__()
        self.__not_visibles__ = set()

    def draw_begin(self):
        self.__reset_size__()
        self.__ent_buffer__.clear()
        self.screen.clear(cv4.TRANSPARENT)
        self.__ent_exist__.clear()

    def draw_insert(self, ent: Entity):
        if ent.surfaceName in self.__not_visibles__:
            return
        if ent.surfaceName not in self.__ent_dict__:
            self.__ent_dict__[ent.surfaceName] = len(self.__ent_dict__)
        self.__ent_buffer__.append(ent)

    def draw_end(self, render_args: RenderArgs):
        render_args.settings = self.__renderOptions__
        for ent in self.__ent_buffer__:
            idx = self.__ent_dict__[ent.surfaceName]
            if idx not in self.__ent_exist__:
                self.buffers[idx].clear(cv4.TRANSPARENT)

            self.__ent_exist__.add(idx)
            render_args.target_surface = self.buffers[idx]
            ent.draw(render_args)
