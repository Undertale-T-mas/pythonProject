from Core.GameArgs import *
from pygame import *
from pygame import Vector2 as vec2
from Core.Animation.ImageSet import *


class Action:
    __fun__: staticmethod | classmethod

    def __init__(self, fun):
        self.__fun__ = fun

    def act(self):
        self.__fun__()


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
        self.image.draw_self(render_args, centre=self.centre)

    image: ImageSetBase | None = None
    surfaceName: str = "default"
    centre: vec2 = vec2(0, 0)
