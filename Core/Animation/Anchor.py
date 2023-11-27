from pygame import Surface
from pygame import Vector2 as vec2

from Core.Animation.ImageSetBase import ImageSetBase
from Core.Animation.AnchorBase import Anchor


class ACustom(Anchor):
    anchor: vec2

    def get_anchor_pos(self) -> vec2:
        return self.anchor


class ACentre(Anchor):
    __imageset__: ImageSetBase

    def __init__(self, img: ImageSetBase):
        self.__imageset__ = img

    def get_anchor_pos(self) -> vec2:
        return self.__imageset__.blockSize / 2.0


class ABottomLeft(Anchor):
    __image__: Surface

    def __init__(self, image: Surface):
        self.__image__ = image

    def get_anchor_pos(self) -> vec2:
        return vec2(0.0, 0.0)