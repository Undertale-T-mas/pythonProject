from Core.Profile.Savable import *
from Game.Map.Framework.TileMap import TileMap
from Game.Map.Framework.WorldData import WorldData
from pygame import Vector2 as vec2


__worldPlayerPosX__ = Savable[float]('global\\loc.ppos.x')
__worldPlayerPosY__ = Savable[float]('global\\loc.ppos.y')
__worldRoomX__ = Savable[int]('global\\loc.room.x')
__worldRoomY__ = Savable[int]('global\\loc.room.y')

if __worldRoomX__.value is None:
    __worldRoomX__.value = -1
if __worldRoomY__.value is None:
    __worldRoomY__.value = -1
if __worldPlayerPosX__.value is None:
    __worldPlayerPosX__.value = 24.0
if __worldPlayerPosY__.value is None:
    __worldPlayerPosY__.value = 0.0


__worldCurRoom__: TileMap


class WorldManager:
    @staticmethod
    def save(player_pos: vec2):
        __worldRoomX__.value = int(__worldCurRoom__.worldPos.x)
        __worldRoomY__.value = int(__worldCurRoom__.worldPos.y)
        __worldPlayerPosX__.value = player_pos.x
        __worldPlayerPosY__.value = player_pos.y

    @staticmethod
    def get_map(x: int, y: int) -> TileMap:
        return WorldData.get_map(x, y)

    @staticmethod
    def change_map(x: int, y: int, speed_remain: vec2):
        pass
