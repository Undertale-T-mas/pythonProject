from Core import GameStates
from pygame import *


class GameArgs:
    elapsedSec = 0.0
    totalSec = 0.0

    def __init__(self):
        pass

    def update(self, time_elapsed: float):
        self.elapsedSec = time_elapsed
        self.totalSec += time_elapsed


class RenderArgs:
    target_surface: surface
