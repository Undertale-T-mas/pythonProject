import pygame
from pygame import Vector2 as vec2


class RenderOptions:
    screenSize: vec2 = vec2(1080, 600)
    surfaceFlag: int = pygame.HWSURFACE
