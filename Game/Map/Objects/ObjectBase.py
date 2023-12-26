from Game.Characters.Humans.Data import IPlayer
from core import *


def __get_player__() -> IPlayer:
    return GameState.__gsScene__.__player__


class MapObjectFuncBase(GameObject):
    _worldPos: vec2 | None
    _id: int | None

    args: GameArgs

    def __init__(self, world_pos: vec2 | None = None, _id: int | None = None):
        self._worldPos = world_pos
        self._id = _id

    @staticmethod
    def image_changed():
        GameState.__gsScene__.tileChanged = True

    def save_path(self) -> str:
        return ('map\\over_world\\' +
                str((int(self._worldPos.x) + 1172) ^ 3815) +
                '_' +
                str((int(self._worldPos.y) + 1536) ^ 2835) +
                '.' +
                str((self._id + 1234) ^ 9017)
                )

    @staticmethod
    def get_player() -> IPlayer:
        return __get_player__()

    def on_create(self, pos_x: int, pos_y: int):
        raise NotImplementedError()

    def on_update(self, object_source: Entity):
        raise NotImplementedError()

    def update(self, args: GameArgs):
        self.args = args
