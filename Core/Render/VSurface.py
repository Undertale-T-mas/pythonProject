from pygame import *

from Core.Entity import Entity
from Core.GameArgs import RenderArgs
from Core.GameObject import *
from typing import *

from Core.GamingGL.GLBase import RenderTarget


class VSurface:
    name: str
    surf: RenderTarget
    visible: bool

    __objs__: List[Entity]

    def reset(self):
        self.__objs__.clear()

    def append(self, ent: Entity):
        self.__objs__.append(ent)

    def draw(self, render_args: RenderArgs):
        if not isinstance(self.surf, RenderTarget):
            raise ValueError()
        render_args.target_surface = self.surf
        for ent in self.__objs__:
            ent.draw(render_args)

    def __init__(self, name: str, surf: RenderTarget):
        self.name = name
        self.visible = True
        self.surf = surf
