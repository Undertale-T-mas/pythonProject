from Core import GameStates
from pygame import *
from pygame import Vector2 as vec2

from Core.GamingGL.GLBase import RenderTarget


class GameArgs:
    elapsedSec = 0.0
    totalSec = 0.0

    def __init__(self):
        pass

    def update(self, time_elapsed: float):
        self.elapsedSec = time_elapsed
        self.totalSec += time_elapsed


EXTREME_QUALITY = 3
HIGH_QUALITY = 2
MED_QUALITY = 1
LOW_QUALITY = 0


class RenderArgs:
    def __init__(self):
        self.quality = EXTREME_QUALITY

    target_surface: RenderTarget
    quality: int
    camera_delta: vec2
