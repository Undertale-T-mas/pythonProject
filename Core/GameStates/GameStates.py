from Core.GameArgs import *
from Core.GameObject import *
from Core.GameStates.ObjectManager import *
from Scene import *
from typing import *

__gsGameArgs__ = GameArgs()
__gsRenderArgs__ = RenderArgs()
__gsScene__: Scene
__gsSceneBuffer__: Scene
__gsSurfaceManager__: SurfaceManager
__gsRenderOptions__: RenderOptions


def initialize(render_options: RenderOptions):
    Core.GameStates.Scene.__gsSurfaceManager__ = SurfaceManager(render_options)
    Core.GameStates.Scene.__gsRenderOptions__ = render_options


def instance_create(obj: GameObject):
    __gsScene__.instance_create(obj)


def change_scene(scene: Scene):
    Core.GameStates.Scene.__gsSceneBuffer__ = scene


def update(time_elapsed: float):
    __gsGameArgs__.update(time_elapsed)
    if not __gsSceneBuffer__ == __gsScene__:
        Core.GameStates.Scene.__gsScene__ = __gsSceneBuffer__
