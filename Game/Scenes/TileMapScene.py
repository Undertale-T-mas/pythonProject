from Core.GameStates.Scene import *
from Core.Profile.ProfileIO import *
from Core.Profile.Savable import Savable
from Game.Map.Framework.TileMap import *


class TileMapScene(Scene):
    tileMap: TileMap
    __difficulty__: Savable[int]
    __diffDynamic__: Savable[float]

    def set_tiles(self, tile_map: TileMap):
        self.tileMap = tile_map
        self.__difficulty__ = Savable[int]('global\\mode.diff.meta')
        self.__diffDynamic__ = Savable[float]('global\\mode.diff.dyna')
        if self.__difficulty__.value is None:
            self.__difficulty__.value = 0
        if self.__diffDynamic__.value is None:
            self.__diffDynamic__.value = 0
        ProfileIO.save()
        self.instance_create(self.tileMap)

    @property
    def scene_difficulty(self):
        return self.__difficulty__.value

