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

    imageSource: Surface
    blockSize: vec2
    indexX: int = 0
    indexY: int = 0
    scale: float = 1.0
    flip: bool = False

    anchor: Anchor

    def source_area(self) -> Rect:
        raise NotImplementedError()

    __idxXLast__: int = 0
    __idxYLast__: int = 0
    __flipLast__: bool = False
    __curScale__: float = 1.0
    __imageDraw__: Surface = None

    def __need_refresh__(self) -> bool:
        if self.__imageDraw__ is None:
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
