from ctypes import *
from typing import Any, List, Dict

import pygame
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GL.shaders import compileShader
from OpenGL.GLUT import *
from numpy import uintc
from pygame import Vector2 as vec2, Surface, Color, Vector3
from Core.MathUtil import Vector4 as vec4
from Core.MathUtil import ColorV4 as cv4
from Core.MathUtil import FRect


__vertexDefault__: Any = None
__glsScreenSize__: vec2 | None = None


def __vertexCompile__():
    global __vertexDefault__
    file = open('Shaders\\Default\\vertex.glsl', 'r')
    source = file.read()
    __vertexDefault__ = compileShader(source, GL_VERTEX_SHADER)
    file.close()


class ITexture:

    texture_id: uintc


class Shader:

    def copy(self):
        res = type(self)()
        res.shader_uid = self.shader_uid
        res.program_uid = self.program_uid
        res.__uniform_loc__ = self.__uniform_loc__
        return res

    __tex_id__: int
    shader_uid: Any
    program_uid: Any
    __uniform_loc__: Dict[str, Any]

    @property
    def screen_size(self):
        return __glsScreenSize__

    @staticmethod
    def print_log(shader):
        length = c_int()
        glGetShaderiv(shader, GL_INFO_LOG_LENGTH, byref(length))

        if length.value > 0:
            log = create_string_buffer(length.value)
            glGetShaderInfoLog(shader, length, byref(length), log)
            print(sys.stderr, log.value)

    def __init__(self, source_path: str | None = None):
        if source_path is None:
            return

        global __vertexDefault__
        if __vertexDefault__ is None:
            __vertexCompile__()

        file = open(source_path, 'r')
        source = file.read()
        self.shader_uid = compileShader(source, GL_FRAGMENT_SHADER)
        self.program_uid = glCreateProgram()
        file.close()

        glAttachShader(self.program_uid, __vertexDefault__)
        glAttachShader(self.program_uid, self.shader_uid)
        glLinkProgram(self.program_uid)

        # 检查链接状态
        status = glGetProgramiv(self.program_uid, GL_LINK_STATUS)
        if status != GL_TRUE:
            raise RuntimeError(glGetProgramInfoLog(self.program_uid))

        self.__tex_id__ = 0
        self.__uniform_loc__ = dict()

    def set_arg(self, arg_name: str, arg: Any):
        if arg_name in self.__uniform_loc__:
            uniform_loc = self.__uniform_loc__[arg_name]
        else:
            uniform_loc = glGetUniformLocation(self.program_uid, arg_name)
            self.__uniform_loc__[arg_name] = uniform_loc

        if isinstance(arg, float):
            glUniform1f(uniform_loc, arg)

        elif isinstance(arg, int):
            glUniform1i(uniform_loc, arg)

        elif isinstance(arg, vec2):
            glUniform2f(uniform_loc, arg.x, arg.y)

        elif isinstance(arg, Vector3):
            glUniform3f(uniform_loc, arg.x, arg.y, arg.z)

        elif isinstance(arg, vec4):
            glUniform4f(uniform_loc, arg.x, arg.y, arg.z, arg.w)

        elif isinstance(arg, ITexture):
            if self.__tex_id__ == 0:
                glActiveTexture(GL_TEXTURE0)
            elif self.__tex_id__ == 1:
                glActiveTexture(GL_TEXTURE1)
            elif self.__tex_id__ == 2:
                glActiveTexture(GL_TEXTURE2)
            elif self.__tex_id__ == 3:
                glActiveTexture(GL_TEXTURE3)
            elif self.__tex_id__ == 4:
                glActiveTexture(GL_TEXTURE4)
            elif self.__tex_id__ == 5:
                glActiveTexture(GL_TEXTURE5)
            elif self.__tex_id__ == 6:
                glActiveTexture(GL_TEXTURE6)
            elif self.__tex_id__ == 7:
                glActiveTexture(GL_TEXTURE7)
            elif self.__tex_id__ == 8:
                glActiveTexture(GL_TEXTURE8)
            elif self.__tex_id__ == 9:
                glActiveTexture(GL_TEXTURE9)
            else:
                raise IndexError()
            glBindTexture(GL_TEXTURE_2D, arg.texture_id)
            glUniform1i(uniform_loc, self.__tex_id__)
            self.__tex_id__ += 1

    def reset(self):
        self.__tex_id__ = 0

    def apply(self):
        glUseProgram(self.program_uid)


class EffectLib:
    motion_blur: Shader
    overlay: Shader
    grid: Shader

    @staticmethod
    def init():
        EffectLib.motion_blur = Shader('Shaders\\Effects\\motion_blur.glsl')
        EffectLib.overlay = Shader('Shaders\\Effects\\overlay.glsl')
        EffectLib.grid = Shader('Shaders\\Effects\\grid.glsl')


class DefaultShaderLib:
    fill: Shader
    blend: Shader

    @staticmethod
    def init():
        # pass
        DefaultShaderLib.blend = Shader('Shaders\\Default\\blend.glsl')
        DefaultShaderLib.fill = Shader('Shaders\\TEST\\fill.glsl')
        EffectLib.init()
