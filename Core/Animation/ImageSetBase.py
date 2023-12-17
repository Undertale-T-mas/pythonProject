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
from Core.MathUtil import Math
from Resources.ResourceLoad import *


class ImageSetBase:

    def copy(self):
        raise NotImplementedError()

    def load(self, path: str):
        self.imageSource = load_image(path)

    __blockSize__: vec2

    @property
    def blockSize(self) -> vec2:
        return self.__blockSize__

    @blockSize.setter
    def blockSize(self, size: vec2):
        self.__blockSize__ = size

    __imageSource__: Surface

    @property
    def imageSource(self) -> Surface:
        return self.__imageSource__

    @imageSource.setter
    def imageSource(self, surf: Surface):
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

    def source_area(self) -> Rect:
        raise NotImplementedError()

    __imageUpdated__: bool
    __idxXLast__: int
    __idxYLast__: int
    __alpha__: float
    __flip__: bool
    __imageDraw__: Surface | None

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

    def __need_refresh__(self) -> bool:
        if self.__imageDraw__ is None or self.__imageUpdated__:
            self.__imageUpdated__ = False
            return True

        if self.__idxYLast__ != self.indexY or self.__idxXLast__ != self.indexX:
            return True

        return False

    def __create_img__(self):
        cur = self.imageSource.subsurface(self.source_area())
        if Math.abs(self.__scale__.length_squared() - 1.0) > 0.0001:
            cur = transform.scale(cur, vec2(self.__scale__.x * cur.get_width(), self.__scale__.y * cur.get_height()))
        if self.flip:
            cur = transform.flip(cur, True, False)
        if Math.abs(1 - self.alpha) > 0.0001:
            cur.set_alpha(int(self.alpha * 255))

        self.__imageDraw__ = cur
        self.__idxXLast__ = self.indexX
        self.__idxYLast__ = self.indexY
        self.__flipLast__ = self.flip

    def draw_self(self, args: RenderArgs, centre: vec2):
        if self.__need_refresh__():
            self.__create_img__()

        a = self.anchor.get_anchor_pos()
        v = centre - vec2(a.x * self.__scale__.x, a.y * self.__scale__.y)

        if not self.stable:
            v -= args.camera_delta

        args.target_surface.blit(
            self.__imageDraw__,
            v
        )
