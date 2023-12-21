import io
import os
from typing import *

from pygame import *
from pygame import Vector2 as vec2

import Resources.ResourceLoad
from Core.Animation.Anchor import *
from Core.GameArgs import *
from Resources.ResourceLoad import *
from Core.Animation.ImageSetBase import *


class SingleImage(ImageSetBase):
    def __init__(self, path: str):
        super().__init__()
        self.__imageSource__ = Texture(load_image(path))
        self.anchor = ACentre(self)
        self.blockSize = vec2(self.__imageSource__.get_width(), self.__imageSource__.get_height())

    def source_area(self):
        size = self.imageSource.get_size()
        return FRect(0, 0, size[0], size[1])


class ImageSet(ImageSetBase):
    __blockDistance__: vec2

    def __init__(self, block_size: vec2, block_distance: vec2, path: str | Texture):
        super().__init__()
        self.blockSize = block_size
        self.__blockDistance__ = block_distance
        self.anchor = ACentre(self)
        if isinstance(path, str):
            self.__imageSource__ = Texture(load_image(path))
        else:
            self.__imageSource__ = path

    def source_area(self):
        x = self.__blockDistance__.x * self.indexX
        y = self.__blockDistance__.y * self.indexY
        return FRect(x, y, self.blockSize.x, self.blockSize.y)

    def copy(self):
        res = ImageSet(self.blockSize, self.__blockDistance__, self.imageSource)
        res.__scale__ = self.__scale__
        return res


class MultiImageSet(ImageSetBase):
    __blockDistance__: vec2

    def __init__(self, block_size: vec2, block_distance: vec2, path: str):
        super().__init__()
        self.imageDict = dict()
        self.imageList = []
        self.load(path)
        self.blockSize = block_size
        self.__blockDistance__ = block_distance
        self.anchor = ACentre(self)

    def source_area(self):
        x = self.__blockDistance__.x * self.indexX
        y = self.__blockDistance__.y * self.indexY
        return FRect(x, y, self.blockSize.x, self.blockSize.y)

    imageDict: Dict[str, Texture]
    imageList: List[Texture]

    def set_image(self, index: int | str):
        if index is int:
            self.__imageSource__ = self.imageList[index]
        elif index is str:
            self.__imageSource__ = self.imageDict[index]

    def load(self, root: str):
        paths = os.listdir('Resources\\Images\\' + root)
        for path in paths:
            if '.' not in path:
                continue
            surf = load_image(root + '\\' + path)
            surf = Texture(surf)
            self.imageDict[path.removesuffix('.png')] = surf
            self.imageList.append(surf)
        self.__imageSource__ = self.imageList[0]


class MultiImage(ImageSetBase):
    def __init__(self,  path: str):
        super().__init__()
        self.imageList = []
        self.imageDict = dict()
        self.load(path)
        self.anchor = ACentre(self)

    @property
    def blockSize(self):
        return vec2(self.__imageSource__.get_width(), self.__imageSource__.get_height())

    def source_area(self):
        return FRect(0, 0, self.__imageSource__.get_width(), self.__imageSource__.get_height())

    imageDict: Dict[str, Texture]
    imageList: List[Texture]

    def set_image(self, index: int | str):
        if isinstance(index, int):
            self.imageSource = self.imageList[index]
        elif isinstance(index, str):
            self.imageSource = self.imageDict[index]

    def load(self, root: str):
        paths = os.listdir('Resources\\Images\\' + root)
        for path in paths:
            surf = load_image(root + '\\' + path)
            surf = Texture(surf)
            self.imageDict[path.removesuffix('.png')] = surf
            self.imageList.append(surf)
        self.__imageSource__ = self.imageList[0]
