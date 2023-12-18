from typing import Any

import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from pygame import Vector2 as vec2, Surface, Color
from Core.MathUtil import Vector4 as vec4
from Core.MathUtil import ColorV4 as cv4
from Core.MathUtil import FRect


__glBufferID__ = 0


class GamingGL:
    @staticmethod
    def set_render_target(fbo_id):
        global __glBufferID__
        if __glBufferID__ == fbo_id:
            return
        __glBufferID__ = fbo_id
        glBindFramebuffer(GL_FRAMEBUFFER, __glBufferID__)

    @staticmethod
    def default_transform(viewport_size: vec2):
        glLoadIdentity()
        glTranslate(-1, -1, 0)
        glScale(2 / viewport_size.x, 2 / viewport_size.y, 1)

    @staticmethod
    def screen_transform(viewport_size: vec2):
        glLoadIdentity()
        glTranslate(-1, 1, 0)
        glScale(2 / viewport_size.x, -2 / viewport_size.y, 1)

    @staticmethod
    def begin(viewport_size: vec2):
        GamingGL.default_transform(viewport_size)
        glEnable(GL_TEXTURE_2D)

    @staticmethod
    def end():
        glDisable(GL_TEXTURE_2D)


class RenderData:
    pos: vec2
    color: vec4 | None
    scale: vec2
    flip: bool
    anchor: vec2 | None
    rotation: float
    texBound: FRect

    def __init__(self, pos: vec2, color: vec4 | None = None,
                 scale: vec2 = vec2(1, 1), flip: bool = False,
                 anchor: vec2 = None, rotation: float = 0.0, bound: FRect = None):
        self.pos = pos
        self.color = color
        self.scale = scale
        self.flip = flip
        self.anchor = anchor
        self.rotation = rotation
        self.texBound = bound


class IRenderTarget:
    _fbo_id: int

    def set_target_self(self):
        GamingGL.set_render_target(self._fbo_id)


class IDrawable:
    def draw(self, data: RenderData):
        raise NotImplementedError()

    def draw_to(self, data: RenderData, target: IRenderTarget):
        target.set_target_self()
        self.draw(data)


class Texture(IDrawable):

    texture_id: int
    width: float
    height: float

    def __init__(self, surface: Surface):
        self.width, self.height = surface.get_size()
        self.texture_id = glGenTextures(1)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     pygame.image.tostring(surface.convert_alpha(), 'RGBA'))

        glBindTexture(GL_TEXTURE_2D, 0)

    def draw(self, render_data: RenderData):
        x, y = render_data.pos.x, render_data.pos.y

        color_enable = render_data.color is not None
        bound = render_data.texBound
        if bound is None:
            bound = FRect(0, 0, self.width, self.height)

        w, h = bound.width * render_data.scale.x, bound.height * render_data.scale.y

        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_QUADS)
        glTexCoord2f(bound.x / self.width, bound.y / self.height)
        glVertex2f(x, y)

        glTexCoord2f(bound.right / self.width, bound.y / self.height)
        glVertex2f(x + w, y)

        glTexCoord2f(bound.right / self.width, bound.bottom / self.height)
        glVertex2f(x + w, y + h)

        glTexCoord2f(bound.x / self.width, bound.bottom / self.height)
        glVertex2f(x, y + h)

        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)


# noinspection PyMissingConstructor
class RenderTarget(IRenderTarget, Texture):

    def set_target_self(self):
        GamingGL.set_render_target(self._fbo_id)

    def __init__(self, width: float | int, height: float | int, is_screen: bool = False):
        self.width = int(width)
        self.height = int(height)

        if is_screen:
            self._fbo_id = 0
            return

        fbo_id = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, fbo_id)

        render_texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, render_texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, render_texture_id, 0)

        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
            print("Error: Unable to create FBO")
            raise Exception()

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, 0)

        self._fbo_id = fbo_id
        self.texture_id = render_texture_id

    def blit(self, img: Texture, pos: vec2, area: FRect | None = None):
        img.draw_to(RenderData(pos, bound=area), self)

    def blit_data(self, img: Texture, data: RenderData):
        img.draw_to(data, self)

    def clear(self, col: vec4):
        self.set_target_self()

        glClearColor(col.x, col.y, col.z, col.w)
        glClear(GL_COLOR_BUFFER_BIT)

