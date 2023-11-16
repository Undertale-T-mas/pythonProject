from Core.GameArgs import *


class GameStates:
    def __init__(self):
        self.gameArgs = GameArgs(self)
        pass

    renderArgs = RenderArgs()
    gameArgs: GameArgs
