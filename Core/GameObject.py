from Core.GameArgs import *
from pygame import *
from pygame import Vector2 as vec2
from Core.Animation.ImageSet import *


class GameObject:
    def update(self, args: GameArgs):
        raise NotImplementedError()

    __disposed__ = False

    def is_disposed(self):
        return self.__disposed__

    def dispose(self):
        self.__disposed__ = True


class Entity(GameObject):
    def draw(self, render_args: RenderArgs):
        raise NotImplementedError()

    image: ImageSetBase
    surfaceName: str = "default"
    centre: vec2 = vec2(0, 0)
