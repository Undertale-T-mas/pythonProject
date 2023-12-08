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
    scale: float
    flip: bool

    anchor: Anchor

    def source_area(self) -> Rect:
        raise NotImplementedError()

    __imageUpdated__: bool
    __idxXLast__: int
    __idxYLast__: int
    __flipLast__: bool
    __curScale__: float
    __imageDraw__: Surface | None

    def __init__(self):
        self.indexX = 0
        self.indexY = 0
        self.scale = 1.0
        self.flip = False
        self.__imageDraw__ = None
        self.__curScale__ = 1.0
        self.__flipLast__ = False
        self.__idxXLast__ = 0
        self.__idxYLast__ = 0
        self.__imageUpdated__ = False

    def __need_refresh__(self) -> bool:
        if self.__imageDraw__ is None or self.__imageUpdated__:
            self.__imageUpdated__ = False
            return True

        if Math.abs(self.scale - self.__curScale__) > 0.0001:
            return True

        if self.__idxYLast__ != self.indexY or self.__idxXLast__ != self.indexX:
            return True

        if self.__flipLast__ != self.flip:
            return True

        return False

    def __create_img__(self):
        cur = self.imageSource.subsurface(self.source_area())
        if Math.abs(self.scale - 1.0) > 0.0001:
            cur = transform.scale(cur, vec2(self.scale * cur.get_width(), self.scale * cur.get_height()))
        if self.flip:
            cur = transform.flip(cur, True, False)
        self.__imageDraw__ = cur
        self.__curScale__ = self.scale
        self.__idxXLast__ = self.indexX
        self.__idxYLast__ = self.indexY
        self.__flipLast__ = self.flip

    def draw_self(self, args: RenderArgs, centre: vec2):
        if self.__need_refresh__():
            self.__create_img__()

        v = centre - self.anchor.get_anchor_pos() * self.scale

        args.target_surface.blit(
            self.__imageDraw__,
            v
        )
