from typing import Any

from Core.Animation.ImageSetBase import ImageSetBase
from Core.GameArgs import RenderArgs
from Core.GameObject import GameObject
from pygame import Vector2 as vec2


class IEntity:
    def draw(self, render_args: RenderArgs):
        raise NotImplementedError()


class Entity(GameObject, IEntity):
    def __init__(self):
        self.image = None
        super().__init__()
        self.surfaceName = 'default'
        self.centre = vec2(0, 0)
        self.visible = True
        self.__extra__ = None

    def draw(self, render_args: RenderArgs):
        self.image.draw_self(render_args, centre=self.centre)

    __extra__: Any
    image: ImageSetBase | None
    surfaceName: str
    centre: vec2
    visible: bool


class EntityEvent:
    __fun__: staticmethod | classmethod

    def __init__(self, fun):
        self.__fun__ = fun

    def act(self, obj: Entity):
        self.__fun__(obj)