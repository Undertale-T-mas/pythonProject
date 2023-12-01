from pygame import *


class CollideArea:
    def CollideWith(self, another) -> bool:
        raise Exception()


class CollideRect(CollideArea):
    area: Rect = Rect(0, 0, 0, 0)

    def CollideWith(self, another) -> bool:
        if isinstance(another, CollideRect):
            return self.area.colliderect(another.area)
        raise NotImplementedError()

