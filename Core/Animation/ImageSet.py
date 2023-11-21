import io
import os
from typing import *

from pygame import *
from pygame import Vector2 as vec2

import Resources.ResourceLoad
from Core.Animation.anchor import Anchor
from Core.GameArgs import *
from Resources import ResourceLoad


class ImageSetBase:

    def load(self, path: str):
        self.imageSource = image.load(path)

    imageSource: Surface
    blockSize: vec2
    indexX: int
    indexY: int

    anchor: Anchor

    def source_area(self) -> Rect:
        raise NotImplementedError()

    def draw_self(self, args: RenderArgs, centre: vec2):
        args.target_surface.blit(
            self.imageSource,
            centre - self.anchor.get_anchor_pos(),
            self.source_area()
        )


class SingleImage(ImageSetBase):

    def source_area(self):
        size = self.imageSource.get_size()
        return Rect(0, 0, size[0], size[1])


class ImageSet(ImageSetBase):
    __blockDistance__: vec2

    def __init__(self, block_size: vec2, block_distance: vec2, path: str):
        self.imageSource = image.load(path)
        self.blockSize = block_size
        self.__blockDistance__ = block_distance

    def source_area(self):
        x = self.__blockDistance__.x * self.indexX
        y = self.__blockDistance__.y * self.indexY
        return Rect(x, y, self.blockSize.x, self.blockSize.y)


class MultiImageSet(ImageSetBase):
    __blockDistance__: vec2

    def __init__(self, block_size: vec2, block_distance: vec2, path: str):
        self.imageSource = image.load(path)
        self.blockSize = block_size
        self.__blockDistance__ = block_distance

    def source_area(self):
        x = self.__blockDistance__.x * self.indexX
        y = self.__blockDistance__.y * self.indexY
        return Rect(x, y, self.blockSize.x, self.blockSize.y)

    imageDict: Dict[str, Surface] = dict()
    imageList: List[Surface] = []

    def set_image(self, index: int | str):
        if index is int:
            self.imageSource = self.imageList[index]
        elif index is str:
            self.imageSource = self.imageDict[index]

    def load(self, path: str):
        paths = os.listdir()
        for path in paths:
            surf = ResourceLoad.load_image(path)
            self.imageDict[path] = surf
            self.imageList.append(surf)
        self.imageSource = self.imageList[0]
