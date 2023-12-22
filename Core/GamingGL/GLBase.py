from typing import Any, List, Dict

import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from numpy import uintc
from pygame import Vector2 as vec2, Surface, Color
import numpy as np
from ctypes import *
from Core.GamingGL.GLShader import *
from Core.MathUtil import Vector4 as vec4
from Core.MathUtil import ColorV4 as cv4
from Core.MathUtil import FRect


__glBufferID__ = 0
__glPosArray__: List[None | vec2] = [None, None, None, None]
__glVAO__ = None
__glVBO__ = None


class GamingGL:
    __viewport__: vec2

    @staticmethod
    def init(viewport_default: vec2):
        global __glVAO__, __glVBO__

        GamingGL.__viewport__ = viewport_default
        DefaultShaderLib.init()
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)

        __glVAO__ = glGenVertexArrays(1)
        __glVBO__ = glGenBuffers(1)

    @staticmethod
    def set_render_target(fbo_id):
        global __glBufferID__
        if __glBufferID__ == fbo_id:
            return
        __glBufferID__ = fbo_id

        if fbo_id == 0:
            GamingGL.screen_transform()
        else:
            GamingGL.default_transform()

        glBindFramebuffer(GL_FRAMEBUFFER, __glBufferID__)

    @staticmethod
    def default_transform(viewport_size: vec2 | None = None):
        if viewport_size is None:
            viewport_size = GamingGL.__viewport__
        glLoadIdentity()
        glTranslate(-1, -1, 0)
        glScale(2 / viewport_size.x, 2 / viewport_size.y, 1)

    @staticmethod
    def screen_transform(viewport_size: vec2 | None = None):
        if viewport_size is None:
            viewport_size = GamingGL.__viewport__
        glLoadIdentity()
        glTranslate(-1, 1, 0)
        glScale(2 / viewport_size.x, -2 / viewport_size.y, 1)

    @staticmethod
    def begin(viewport_size: vec2 | None = None):
        GamingGL.default_transform(viewport_size)
        glEnable(GL_TEXTURE_2D)

    @staticmethod
    def end():
        glDisable(GL_TEXTURE_2D)


class BlendState:
    factor_src: Any
    factor_dst: Any

    def __init__(self, src: Any, dst: Any):
        self.factor_src = src
        self.factor_dst = dst


class RenderData:
    pos: vec2
    color: vec4 | None
    scale: vec2
    flip: bool
    anchor: vec2 | None
    rotation: float
    texBound: FRect
    blend: BlendState | None

    def __init__(self, pos: vec2, color: vec4 | None = None,
                 scale: vec2 = vec2(1, 1), flip: bool = False,
                 anchor: vec2 = None, rotation: float = 0.0, bound: FRect = None,
                 blend: BlendState | None = None):
        self.pos = pos
        if color is not None:
            if color != vec4(1, 1, 1, 1):
                self.color = color
            else:
                self.color = None
        else:
            self.color = None
        self.scale = scale
        self.flip = flip
        self.blend = blend
        self.anchor = anchor
        self.rotation = rotation
        self.texBound = bound


class IRenderTarget:
    _fbo_id: int

    def set_target_self(self):
        GamingGL.set_render_target(self._fbo_id)

    def get_width(self):
        raise NotImplementedError()

    def get_height(self):
        raise NotImplementedError()


class IDrawable(ITexture):
    def draw(self, data: RenderData):
        raise NotImplementedError()

    def draw_to(self, data: RenderData, target: IRenderTarget):
        target.set_target_self()
        self.draw(data)


__glListMemTmp__: List[Any] = [None, None, None, None]
__glTexCoordList__: List[Any] = [vec2(0, 0), vec2(1, 0), vec2(1, 1), vec2(0, 1)]

__glTextureMem__: Dict[int, uintc] = dict()
__glBufferList__: List[Any] = []


def __glPushArray__():
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)

    glBindVertexArray(__glVAO__)
    glBindBuffer(GL_ARRAY_BUFFER, __glVBO__)
    __glBufferList__.clear()
    for i in range(4):
        __glBufferList__.append(__glPosArray__[i].x)
        __glBufferList__.append(__glPosArray__[i].y)
        __glBufferList__.append(0)
        __glBufferList__.append(__glTexCoordList__[i].x)
        __glBufferList__.append(__glTexCoordList__[i].y)

    vertices = np.array(__glBufferList__, dtype=np.float32)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
# 设置顶点数据
    vertices = np.array(__glPosArray__, dtype=np.float32)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    # 设置纹理坐标数据
    tex_coords = np.array(__glTexCoordList__, dtype=np.float32)
    glBufferData(GL_ARRAY_BUFFER, tex_coords.nbytes, tex_coords, GL_STATIC_DRAW)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)

    glDrawArrays(GL_TRIANGLES, 0, 6)

    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)


class Texture(IDrawable):

    width: float
    height: float

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_size(self):
        return self.width, self.height

    @property
    def centre(self):
        return vec2(self.width / 2, self.height / 2)

    def __init__(self, surface: Surface):
        self.width, self.height = surface.get_size()

        dat = pygame.image.tostring(surface.convert_alpha(), 'RGBA')
        h = hash(dat)
        if h in __glTextureMem__:
            self.texture_id = __glTextureMem__[h]
            return

        self.texture_id = glGenTextures(1)
        __glTextureMem__[h] = self.texture_id

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE,
                     dat)

        glBindTexture(GL_TEXTURE_2D, 0)

    def draw(self, render_data: RenderData):
        mode = False

        x, y = render_data.pos.x, render_data.pos.y

        if render_data.blend is not None:
            glEnable(GL_BLEND)
            glBlendFunc(render_data.blend.factor_src, render_data.blend.factor_dst)

        color_enable = render_data.color is not None
        coord_list = __glTexCoordList__
        bound = render_data.texBound
        if bound is None:
            bound = FRect(0, 0, self.width, self.height)
        else:
            coord_list = __glListMemTmp__
            coord_list[0] = vec2(bound.x / self.width, bound.y / self.height)
            coord_list[1] = vec2(bound.right / self.width, bound.y / self.height)
            coord_list[2] = vec2(bound.right / self.width, bound.bottom / self.height)
            coord_list[3] = vec2(bound.x / self.width, bound.bottom / self.height)

        w, h = bound.width * render_data.scale.x, bound.height * render_data.scale.y
        if render_data.anchor is not None:
            if render_data.anchor.length_squared() > 0.001:
                x -= render_data.anchor.x * render_data.scale.x
                y -= render_data.anchor.y * render_data.scale.y

        col = render_data.color
        if col is None:
            col = vec4(1, 1, 1, 1)

        DefaultShaderLib.blend.apply()
        DefaultShaderLib.blend.set_arg('blend_color', col)
        DefaultShaderLib.blend.set_arg('sampler', self)
        DefaultShaderLib.blend.set_arg('screen_size', GamingGL.__viewport__)

        if render_data.flip:
            if not mode:
                glBegin(GL_QUADS)
            __glTexCoordList__[0] = vec2(coord_list[1].x, coord_list[1].y)
            __glPosArray__[0] = vec2(x, y)

            __glTexCoordList__[1] = vec2(coord_list[0].x, coord_list[0].y)
            __glPosArray__[1] = vec2(x + w, y)

            __glTexCoordList__[2] = vec2(coord_list[3].x, coord_list[3].y)
            __glPosArray__[2] = vec2(x + w, y + h)

            __glTexCoordList__[3] = vec2(coord_list[2].x, coord_list[2].y)
            __glPosArray__[3] = vec2(x, y + h)

        else:
            if not mode:
                glBegin(GL_QUADS)
            __glTexCoordList__[0] = vec2(coord_list[0].x, coord_list[0].y)
            __glPosArray__[0] = vec2(x, y)

            __glTexCoordList__[1] = vec2(coord_list[1].x, coord_list[1].y)
            __glPosArray__[1] = vec2(x + w, y)

            __glTexCoordList__[2] = vec2(coord_list[2].x, coord_list[2].y)
            __glPosArray__[2] = vec2(x + w, y + h)

            __glTexCoordList__[3] = vec2(coord_list[3].x, coord_list[3].y)
            __glPosArray__[3] = vec2(x, y + h)

        if __glBufferID__ == 0:
            for i in range(4):
                __glPosArray__[i].y = GamingGL.__viewport__.y - __glPosArray__[i].y

        if mode:
            __glPushArray__()
        if not mode:
            for i in range(4):
                glVertex4f(__glPosArray__[i].x, __glPosArray__[i].y, __glTexCoordList__[i].x, __glTexCoordList__[i].y)
                glTexCoord2f(__glTexCoordList__[i].x, __glTexCoordList__[i].y)

        if not mode:
            glEnd()

        if render_data.blend is not None:
            glDisable(GL_BLEND)

        glUseProgram(0)
        DefaultShaderLib.blend.reset()

        glBindTexture(GL_TEXTURE_2D, 0)


# noinspection PyMissingConstructor
class RenderTarget(IRenderTarget, Texture):
    _fbo_id: Any

    def get_id(self):
        return self._fbo_id

    def set_target_self(self):
        GamingGL.set_render_target(self._fbo_id)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def __init__(self, width: float | int, height: float | int, is_screen: bool = False):
        self.width = int(width)
        self.height = int(height)

        if is_screen:
            GamingGL.init(vec2(width, height))
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
        img.draw_to(RenderData(pos, bound=area, color=cv4.WHITE), self)

    def blit_data(self, img: Texture, data: RenderData):
        img.draw_to(data, self)

    def clear(self, col: vec4):
        self.set_target_self()

        glClearColor(col.x, col.y, col.z, col.w)
        glClear(GL_COLOR_BUFFER_BIT)

    def copy_to(self, target: IRenderTarget):
        src_fbo = self._fbo_id
        dst_fbo = target._fbo_id
        if src_fbo == dst_fbo:
            return

        glBindFramebuffer(GL_READ_FRAMEBUFFER, src_fbo)
        glBindFramebuffer(GL_DRAW_FRAMEBUFFER, dst_fbo)

        src_rect = [0, 0, self.width, self.height]
        dst_rect = [0, 0, target.get_width(), target.get_height()]

        if self._fbo_id == 0 or target._fbo_id == 0:
            glBlitFramebuffer(src_rect[0], src_rect[1], src_rect[2], src_rect[3],
                              dst_rect[0], dst_rect[3], dst_rect[2], dst_rect[1],
                              GL_COLOR_BUFFER_BIT, GL_NEAREST)

        else:
            glBlitFramebuffer(src_rect[0], src_rect[1], src_rect[2], src_rect[3],
                              dst_rect[0], dst_rect[1], dst_rect[2], dst_rect[3],
                              GL_COLOR_BUFFER_BIT, GL_NEAREST)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        return target

