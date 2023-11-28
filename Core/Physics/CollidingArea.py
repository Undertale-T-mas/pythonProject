from pygame import *


class CollideArea:
    def CollideWith(self, another):
        raise Exception()


class CollideRect:
    area: Rect

    def CollideWith(self, another) -> bool:
        if isinstance(another, CollideRect):
            return self.area.colliderect(another.area)
        raise NotImplementedError()

