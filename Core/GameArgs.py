from Core import GameStates


class GameArgs:
    elapsedSec = 0.0
    totalSec = 0.0
    gameStates: GameStates

    def __init__(self, gs: GameStates):
        self.gameStates = gs

    def update(self, time_elapsed: float):
        self.elapsedSec = time_elapsed
        self.totalSec += time_elapsed


class RenderArgs:
    pass
