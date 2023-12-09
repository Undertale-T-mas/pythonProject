from Core.GameStates.Scene import *
from Core.Profile.ProfileIO import *
from Core.Profile.Savable import Savable
from Game.Map.Framework.TileMap import *


class TileMapScene(Scene):
    tileMap: TileMap
    __difficulty__: Savable[int]
    __diffDynamic__: Savable[float]
    tileChanged: bool

    def __init__(self):
        super().__init__()
        self.tileChanged = False

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

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.tileChanged = self.tileMap.tileChanged
        self.tileMap.visible = self.tileChanged

    @property
    def scene_difficulty(self):
        return self.__difficulty__.value

