from pygame.key import *

from Core.GameArgs import *
from Core.GameObject import *
from Core.GameStates.ObjectManager import *
from Core.GameStates.Scene import *
from typing import *

__gsGameArgs__ = GameArgs()
__gsRenderArgs__ = RenderArgs()
__gsScene__: Scene = None
__gsSceneBuffer__: Scene = None
__gsSurfaceManager__: SurfaceManager
__gsRenderOptions__: RenderOptions
__gsKeyStates__: ScancodeWrapper
__gsKeyLast__: ScancodeWrapper


def set_display(render_options: RenderOptions) -> Surface:
    return pygame.display.set_mode(render_options.screenSize)


def initialize(render_options: RenderOptions):
    global __gsSurfaceManager__
    global __gsRenderOptions__
    __gsSurfaceManager__ = SurfaceManager(render_options)
    __gsRenderOptions__ = render_options
    set_display(render_options)


def instance_create(obj: GameObject):
    __gsScene__.instance_create(obj)


def change_scene(scene: Scene):
    global __gsSceneBuffer__
    global __gsScene__
    __gsSceneBuffer__ = scene
    if __gsScene__ is None:
        __gsScene__ = __gsSceneBuffer__


def render():
    __gsScene__.draw(__gsSurfaceManager__)


def update(time_elapsed: float):
    global __gsSceneBuffer__
    global __gsScene__
    global __gsKeyStates__
    global __gsKeyLast__
    __gsKeyStates__ = key.get_pressed()
    __gsGameArgs__.update(time_elapsed)
    if not __gsSceneBuffer__ == __gsScene__:
        __gsScene__ = __gsSceneBuffer__
    __gsScene__.update(__gsGameArgs__)
    __gsKeyLast__ = __gsKeyStates__


def key_hold(key_id):
    return __gsKeyStates__[key_id]


def key_on_press(key_id):
    return __gsKeyStates__[key_id] and not __gsKeyLast__[key_id]