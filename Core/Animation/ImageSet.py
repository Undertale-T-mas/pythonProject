from pygame import *
from pygame import Vector2 as vec2


class ImageSetBase:

    imageSource: image
    blockSize: vec2
    indexX: int
    indexY: int

    def destination_area(self):
        raise NotImplementedError()


class ImageSet(ImageSetBase):

    __blockDistance__: vec2

    def __init__(self, block_size: vec2, block_distance: vec2, path: str):
        self.imageSource = image.load(path)
        self.blockSize = block_size
        self.__blockDistance__ = block_distance

    def destination_area(self):
        x = self.__blockDistance__.x * self.indexX
        y = self.__blockDistance__.y * self.indexY
        return Rect(x, y, self.blockSize.x, self.blockSize.y)
