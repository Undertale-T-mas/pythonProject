from pygame.key import *

from Core.GameArgs import *
from Core.GameObject import *
from Core.GameStates.KeyIdentity import KeyIdentity
from Core.GameStates.ObjectManager import *
from Core.GameStates.Scene import *
from typing import *

from Core.GamingGL.GLBase import *
from Core.Render.SurfaceManager import SurfaceManager


__gsGameStop__: bool = False
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

    def copy_with_transform():

        ro = __gsRenderOptions__.transform

        src = __gsSurfaceManager__.screen
        dst = __gsSurfaceManager__.display

        sz = __gsRenderOptions__.screenSize

        GamingGL.screen_transform()
        dst.set_target_self()

        EffectLib.transform.apply()
        EffectLib.transform.set_arg('iCentreUV', ro.centre_uv)
        EffectLib.transform.set_arg('iOffset', ro.offset)
        EffectLib.transform.set_arg('iAlpha', ro.alpha)
        EffectLib.transform.set_arg('iRotation', ro.rotation)
        EffectLib.transform.set_arg('iScale', ro.scale)
        EffectLib.transform.set_arg('screen_size', sz)
        EffectLib.transform.set_arg('sampler', src)

        glBegin(GL_QUADS)

        data = [vec4(0, sz.y, 0, 0), vec4(sz.x, sz.y, 1, 0),
                vec4(sz.x, 0, 1, 1), vec4(0, 0, 0, 1)]
        for i in range(4):
            glVertex4f(data[i].x, data[i].y, data[i].z, data[i].w)
            glTexCoord2f(data[i].z, data[i].w)

        glEnd()

        EffectLib.transform.reset()

    if __gsRenderOptions__.extraBuffer:

        __gsSurfaceManager__.display.clear(cv4.TRANSPARENT)

        if __gsRenderOptions__.transform.check_necessity():
            copy_with_transform()
        else:
            __gsSurfaceManager__.screen.copy_to(__gsSurfaceManager__.display)


def update(time_elapsed: float) -> bool:
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
    return __gsGameStop__


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


def stop_game():
    global __gsGameStop__
    __gsGameStop__ = True
