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


class DelayedAction(GameObject):
    __action__: Action
    __delay__: float

    def __init__(self, delay: float, action: Action):
        self.__delay__ = delay
        self.__action__ = action

    def update(self, args: GameArgs):
        self.__delay__ -= args.elapsedSec
        if self.__delay__ <= 0:
            self.dispose()
            self.__action__.act()


class Entity(GameObject):
    def __init__(self):
        self.image = None
        self.surfaceName = 'default'
        self.centre = vec2(0, 0)
        self.visible = True

    def draw(self, render_args: RenderArgs):
        self.image.draw_self(render_args, centre=self.centre)

    image: ImageSetBase | None
    surfaceName: str
    centre: vec2
    visible: bool
