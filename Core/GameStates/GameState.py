from pygame.key import *

from Core.GameArgs import *
from Core.GameObject import *
from Core.GameStates.KeyIdentity import KeyIdentity
from Core.GameStates.ObjectManager import *
from Core.GameStates.Scene import *
from typing import *
from Core.Render.SurfaceManager import SurfaceManager

__gsGameArgs__ = GameArgs()
__gsRenderArgs__ = RenderArgs()
__gsScene__: Scene | Any = None
__gsSceneBuffer__: Scene | Any = None

__gsSurfaceManager__: SurfaceManager
__gsRenderOptions__: RenderOptions
__gsKeyStates__: ScancodeWrapper
__gsKeyLast__: ScancodeWrapper

__gsInsBuffer__: List[GameObject] = []


def initialize(render_options: RenderOptions):
    global __gsSurfaceManager__
    global __gsRenderOptions__
    __gsSurfaceManager__ = SurfaceManager(render_options)
    __gsRenderOptions__ = render_options


def instance_create(obj: GameObject):
    __gsScene__.instance_create(obj)


def instance_prepare(obj: GameObject):
    __gsInsBuffer__.append(obj)


def change_scene(scene: Scene):
    global __gsSceneBuffer__
    global __gsScene__
    __gsSceneBuffer__ = scene
    if __gsScene__ is None:
        __gsScene__ = __gsSceneBuffer__
    __gsSceneBuffer__.__gsDataSend__(__gsRenderOptions__)


def render():
    __gsScene__.draw(__gsSurfaceManager__)
    if __gsRenderOptions__.extraBuffer:
        __gsSurfaceManager__.display.blit(__gsSurfaceManager__.screen, vec2(0, 0))


def update(time_elapsed: float):
    global __gsSceneBuffer__
    global __gsScene__
    global __gsKeyStates__
    global __gsKeyLast__
    __gsKeyStates__ = key.get_pressed()
    __gsGameArgs__.update(time_elapsed)
    if not __gsSceneBuffer__ == __gsScene__:
        __gsScene__ = __gsSceneBuffer__

    for obj in __gsInsBuffer__:
        __gsScene__.instance_create(obj)
    __gsInsBuffer__.clear()
    __gsScene__.update(__gsGameArgs__)
    __gsKeyLast__ = __gsKeyStates__


def current_scene() -> Scene:
    return __gsScene__


def key_hold(key_id):
    if isinstance(key_id, KeyIdentity):
        for _id in key_id.value:
            if __gsKeyStates__[_id]:
                return True
        return False
    else:
        raise Exception()


def key_on_press(key_id: KeyIdentity):
    if isinstance(key_id, KeyIdentity):
        for _id in key_id.value:
            if __gsKeyStates__[_id] and not __gsKeyLast__[_id]:
                return True
        return False
    else:
        raise Exception()