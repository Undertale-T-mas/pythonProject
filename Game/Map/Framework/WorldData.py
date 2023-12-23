from Core.Entity import Entity
from Core.Profile.Savable import Savable


__map_array__: dict = dict()
__world_difficulty__ = Savable[int]('global\\mode.diff.meta')
__world_difficulty_adjust__ = Savable[float]('global\\mode.diff.dyna')

__worldPlayerPosX__ = Savable[float]('global\\loc.ppos.x')
__worldPlayerPosY__ = Savable[float]('global\\loc.ppos.y')
__worldRoomX__ = Savable[int]('global\\loc.room.x')
__worldRoomY__ = Savable[int]('global\\loc.room.y')


class WorldData:

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
