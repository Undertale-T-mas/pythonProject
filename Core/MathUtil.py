import math
from pygame import Vector2 as vec2
import pygame.rect
import random

rander = random.Random()


class Math:
    @staticmethod
    def sin(val: float) -> float:
        return math.sin(val)

    @staticmethod
    def sin_deg(val: float) -> float:
        return math.sin(val * math.pi / 180.0)

    @staticmethod
    def cos_deg(val: float) -> float:
        return math.cos(val * math.pi / 180.0)

    @staticmethod
    def abs(val: float) -> float:
        if val > 0:
            return val
        return -val

    @staticmethod
    def damage(damage_level: int, defense_level: int) -> float:
        val = (damage_level + 1) * 8.0
        eff = ((defense_level + 2) * 8.0 - pow(val, 0.5)) / (val + 24)
        if eff > 0:
            val *= (1 - min(1, eff))
        return val

    @staticmethod
    def rand(l: int, r: int):
        return rander.randint(l, r)

    @staticmethod
    def vec2_polar(dist: float, deg: float):
        return vec2(Math.cos_deg(deg) * dist, Math.sin_deg(deg) * dist)

    @staticmethod
    def clamp(val, min_v, max_v):
        return max(min(val, max_v), min_v)


class FRect:
    x: float
    y: float
    width: float
    height: float

    def __init__(self, *args):
        if len(args) == 4:
            self.__init0__(args[0], args[1], args[2], args[3])
        elif len(args) == 2:
            self.__init1__(args[0], args[1])
        elif len(args) == 1:
            self.__init2__(args[0])
        else:
            raise Exception()

    def __init0__(self, x: float | int, y: float | int, w: float | int, h: float | int):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def __init1__(self, pos: vec2, size: vec2):
        self.x = pos.x
        self.y = pos.y
        self.width = size.x
        self.height = size.y

    def __init2__(self, rect: any):
        self.x = rect.x
        self.y = rect.y
        self.width = rect.width
        self.height = rect.height

    @property
    def left(self):
        return self.x

    @property
    def i_left(self):
        return int(self.x)

    @property
    def right(self):
        return self.x + self.width

    @property
    def i_right(self):
        return int(self.x + self.width)

    @property
    def top(self):
        return self.y

    @property
    def i_top(self):
        return int(self.y)

    @property
    def bottom(self):
        return self.y + self.height

    @property
    def i_bottom(self):
        return int(self.y + self.height)

    def collide_rect(self, another: any):
        return (self.right > another.left and self.left < another.right and
                self.bottom > another.top and self.top < another.bottom)

    @property
    def size(self):
        return vec2(self.width, self.height)

    @property
    def centre(self):
        return vec2(self.x + self.width / 2, self.y + self.height / 2)

    @size.setter
    def size(self, val: vec2):
        self.width = val.x
        self.height = val.y

    @centre.setter
    def centre(self, centre: vec2):
        self.x = centre.x - self.width / 2
        self.y = centre.y - self.height / 2

    def move(self, x: float, y: float):
        res = FRect(self)
        res.x += x
        res.y += y
        return res