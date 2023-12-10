from Core.GameStates.Scene import *
from Core.Profile.ProfileIO import *
from Core.Profile.Savable import Savable
from Game.Map.Framework.TileMap import *


class TileMapScene(Scene):
    tileMap: TileMap
    __difficulty__: int
    __diffDynamic__: float
    tileChanged: bool

    def __init__(self):
        super().__init__()
        self.tileChanged = False

    def set_tiles(self, tile_map: TileMap):
        self.tileMap = tile_map
        self.__difficulty__ = WorldData.get_difficulty()
        self.__diffDynamic__ = WorldData.get_difficulty_adjust()
        ProfileIO.save()
        self.instance_create(self.tileMap)

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.tileChanged = self.tileMap.tileChanged
        self.tileMap.visible = self.tileChanged

    @property
    def scene_difficulty(self):
        return self.__difficulty__

