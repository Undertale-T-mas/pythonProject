import io
import os
from typing import *

from pygame import *
from pygame import Vector2 as vec2

import Resources.ResourceLoad
from Core.Animation.Anchor import *
from Core.GameArgs import *
from Resources.ResourceLoad import *


class SingleImage(ImageSetBase):

    def source_area(self):
        size = self.imageSource.get_size()
        return Rect(0, 0, size[0], size[1])


class ImageSet(ImageSetBase):
    __blockDistance__: vec2

    def __init__(self, block_size: vec2, block_distance: vec2, path: str):
        self.imageSource = load_image('Tiles\\' + path)
        self.blockSize = block_size
        self.__blockDistance__ = block_distance
        self.anchor = ACentre(self)

    def source_area(self):
        x = self.__blockDistance__.x * self.indexX
        y = self.__blockDistance__.y * self.indexY
        return Rect(x, y, self.blockSize.x, self.blockSize.y)


class MultiImageSet(ImageSetBase):
    __blockDistance__: vec2

    def __init__(self, block_size: vec2, block_distance: vec2, path: str):
        self.load(path)
        self.blockSize = block_size
        self.__blockDistance__ = block_distance
        self.anchor = ACentre(self)

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

    def load(self, root: str):
        paths = os.listdir('Resources\\Images\\' + root)
        for path in paths:
            surf = load_image(root + '\\' + path)
            self.imageDict[path.removesuffix('.png')] = surf
            self.imageList.append(surf)
        self.imageSource = self.imageList[0]
