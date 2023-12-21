import pygame
from pygame import Vector2 as vec2


class RenderOptions:
    screenSize: vec2 = vec2(1056, 600)
    surfaceFlag: int = pygame.HWSURFACE | pygame.SRCALPHA
    renderTargetFlag: int = pygame.OPENGL | pygame.DOUBLEBUF
    extraBuffer: bool = True
    motionBlurEnabled: bool = True
