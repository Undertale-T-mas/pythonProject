from Game.Map.Framework.Tiles import *
from typing import *


class TileMap(Entity):
    tiles: List[List[Tile]] = []

    width: int = -1
    height: int = -1

    def __init__(self):
        self.surfaceName = 'bg'

    def __extend__(self, x: int, y: int):
        while y > self.height:
            self.height += 1
            self.tiles.append([])
        if x > self.width:
            for y in range(self.height + 1):
                for i in range(x - self.width):
                    self.tiles[y].append(Tile(TileLibrary.empty))
            self.width = x

    def set_tile(self, x: int, y: int, tile: Tile):
        self.__extend__(x, y)
        self.tiles[y][x] = tile
        tile.locX = x
        tile.locY = y

    def get_tile(self, x: int, y: int) -> Tile:
        return self.tiles[y][x]

    def update(self, args: GameArgs):
        for i in self.tiles:
            for j in i:
                j.update(args)

    def draw(self, args: RenderArgs):
        for i in self.tiles:
            for j in i:
                j.draw(args)

    pass
