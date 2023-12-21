import io
import os
from typing import *

import pygame
from pygame import *
from pygame import Vector2 as vec2
from pygame.transform import rotate

import Resources.ResourceLoad
from Core.Animation.AnchorBase import Anchor
from Core.GameArgs import *
from Core.GamingGL.GLBase import *
from Core.MathUtil import Math
from Resources.ResourceLoad import *


class ImageSetBase:

    def copy(self):
        raise NotImplementedError()

    def load(self, path: str):
        self.imageSource = Texture(load_image(path))

    __blockSize__: vec2

    @property
    def blockSize(self) -> vec2:
        return self.__blockSize__

    @blockSize.setter
    def blockSize(self, size: vec2):
        self.__blockSize__ = size

    __imageSource__: Texture

    @property
    def imageSource(self) -> Texture:
        return self.__imageSource__

    @imageSource.setter
    def imageSource(self, surf: Texture):
        if surf is self.__imageSource__:
            return
        self.__imageSource__ = surf
        self.__imageUpdated__ = True

    indexX: int
    indexY: int
    __scale__: vec2
    stable: bool

    @property
    def scale(self) -> vec2 | float:
        if self.__scale__.x == self.__scale__.y:
            return self.__scale__.x
        return self.__scale__

    @scale.setter
    def scale(self, val: float | vec2):
        self.__imageUpdated__ = True
        if isinstance(val, vec2):
            self.__scale__ = val
        else:
            self.scale = vec2(val, val)

    @property
    def alpha(self) -> float:
        return self.__alpha__

    @alpha.setter
    def alpha(self, val: float):
        self.__alpha__ = val
        self.__imageUpdated__ = True

    @property
    def flip(self) -> bool:
        return self.__flip__

    @flip.setter
    def flip(self, val: bool):
        if val == self.__flip__:
            return
        self.__flip__ = val
        self.__imageUpdated__ = True

    anchor: Anchor

    def source_area(self) -> FRect:
        raise NotImplementedError()

    __imageUpdated__: bool
    __idxXLast__: int
    __idxYLast__: int
    __alpha__: float
    __flip__: bool
    __imageDraw__: Texture | None

    def __init__(self):
        self.indexX = 0
        self.indexY = 0
        self.scale = 1.0
        self.__flip__ = False
        self.__alpha__ = 1.0
        self.__imageDraw__ = None
        self.__idxXLast__ = 0
        self.__idxYLast__ = 0
        self.__imageUpdated__ = False
        self.stable = False

    def __get_color__(self):
        if self.__alpha__ >= 0.999999:
            return cv4.WHITE
        return vec4(1, 1, 1, self.__alpha__)

    def draw_self(self, args: RenderArgs, centre: vec2):
        a = self.anchor.get_anchor_pos()
        v = vec2(centre.x, centre.y)

        if not self.stable:
            v -= args.camera_delta

        self.__imageDraw__ = self.__imageSource__
        if self.__alpha__ <= 0.00001:
            return
        args.target_surface.blit_data(
            self.__imageDraw__,
            RenderData(v, scale=self.__scale__, flip=self.__flip__, color=self.__get_color__(),
                       anchor=self.anchor.get_anchor_pos(), bound=self.source_area())
        )
