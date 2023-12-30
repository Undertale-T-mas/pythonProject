from typing import Any

from Core.Entity import Entity
from Core.GameStates.GameState import change_scene
from Core.Profile.Savable import Savable


__map_array__: dict = dict()
__world_difficulty__ = Savable[int]('global\\mode.diff.meta')
__world_difficulty_adjust__ = Savable[float]('global\\mode.diff.dyna')

__worldPlayerPosX__ = Savable[float]('global\\loc.ppos.x')
__worldPlayerPosY__ = Savable[float]('global\\loc.ppos.y')
__worldRoomX__ = Savable[int]('global\\loc.room.x')
__worldRoomY__ = Savable[int]('global\\loc.room.y')

__startType__: type
__timeTot__: float
__deathTot__: float


def __set_start_type__(t: type):
    global __startType__
    __startType__ = t


def __wdTransfer__(data: Any):
    global __timeTot__, __deathTot__
    __timeTot__ = data[0]
    __deathTot__ = data[1]


class WorldData:

    @staticmethod
    def get_time_tot():
        return __timeTot__

    @staticmethod
    def get_death_tot():
        return __deathTot__

    @staticmethod
    def insert(single_map: Entity, x: int, y: int):
        pos = ((x + 10) << 10) + y
        if pos in __map_array__.keys():
            return
        __map_array__[pos] = single_map
        pass

    @staticmethod
    def get_map(x: int, y: int):
        tar = __map_array__[((x + 10) << 10) + y]
        return type(tar)()

    @staticmethod
    def exist_map(x: int, y: int):
        return ((x + 10) << 10) + y in __map_array__

    @staticmethod
    def get_difficulty():
        return __world_difficulty__.value

    @staticmethod
    def get_difficulty_adjust():
        return __world_difficulty_adjust__.value

    @classmethod
    def back_to_menu(cls):
        change_scene(__startType__())
