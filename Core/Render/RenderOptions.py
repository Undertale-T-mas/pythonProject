import pygame
from pygame import Vector2 as vec2


class TransformOption:
    rotation: float
    scale: float
    alpha: float
    centre_uv: vec2
    offset: vec2

    def __init__(self):
        self.rotation = 0.0
        self.scale = 1.0
        self.alpha = 1.0
        self.centre_uv = vec2(0.5, 0.5)
        self.offset = vec2(0, 0)

    def check_necessity(self):
        if self.rotation != 0.0 or self.scale != 1.0 or self.alpha != 1.0:
            return True
        if (self.centre_uv - vec2(0.5, 0.5)).length_squared() > 0.0:
            return True
        if self.offset.length_squared() > 0.0:
            return True
        return False


class RenderOptions:

    def __init__(self):
        self.screenSize = vec2(1056, 600)
        self.surfaceFlag = pygame.HWSURFACE | pygame.SRCALPHA
        self.renderTargetFlag = pygame.OPENGL | pygame.DOUBLEBUF
        self.extraBuffer = True
        self.motionBlurEnabled = True
        self.transform = TransformOption()

    screenSize: vec2
    surfaceFlag: int
    renderTargetFlag: int
    extraBuffer: bool
    motionBlurEnabled: bool

    transform: TransformOption

