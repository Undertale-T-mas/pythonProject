from pygame import *


class CollideArea:
    def CollideWith(self, another):
        raise Exception()


class CollideRect:
    area: Rect

    def CollideWith(self, another: Rect):
        return self.area.colliderect(another)

