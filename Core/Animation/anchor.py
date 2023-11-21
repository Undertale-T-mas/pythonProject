from pygame import Surface
from pygame import Vector2 as vec2


class Anchor:
    def get_anchor_pos(self) -> vec2:
        pass


class ACustom(Anchor):
    anchor: vec2

    def get_anchor_pos(self) -> vec2:
        return self.anchor


class ACentre(Anchor):
    __image__: Surface

    def __init__(self, image: Surface):
        self.__image__ = image

    def get_anchor_pos(self) -> vec2:
        return vec2(self.__image__.get_size()) / 2.0


class ABottomLeft(Anchor):
    __image__: Surface

    def __init__(self, image: Surface):
        self.__image__ = image

    def get_anchor_pos(self) -> vec2:
        return vec2(0.0, 0.0)