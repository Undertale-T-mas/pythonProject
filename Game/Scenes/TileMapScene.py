from Core.GameStates.Scene import *
from Game.Map.Framework.TileMap import *


class TileMapScene(Scene):
    tileMap: TileMap

    def set_tiles(self, tile_map: TileMap):
        self.tileMap = tile_map
        self.instance_create(self.tileMap)