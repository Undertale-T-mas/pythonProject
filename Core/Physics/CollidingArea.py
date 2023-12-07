from pygame import *

from Core.MathUtil import FRect


class CollideArea:
    def CollideWith(self, another) -> bool:
        raise Exception()


class CollideRect(CollideArea):
    area: FRect = FRect(0, 0, 0, 0)

    def CollideWith(self, another) -> bool:
        if isinstance(another, CollideRect):
            return self.area.collide_rect(another.area)
        raise NotImplementedError()

