from Game.Map.Framework.Tiles import *
from typing import *


class TileMap(Entity):
    worldPos: vec2
    tiles: List[List[Tile]] = []

    width: int = 0
    height: int = 0

    def __init__(self):
        self.surfaceName = 'bg'

    def __extend__(self, x: int, y: int):
        while y >= self.height:
            self.height += 1
            row = []
            for i in range(self.width):
                row.append(Tile(TileLibrary.empty))
            self.tiles.append(row)

        if x >= self.width:
            for y in range(self.height):
                for i in range(x - self.width + 1):
                    self.tiles[y].append(Tile(TileLibrary.empty))
            self.width = x

    def set_tile(self, x: int, y: int, tile: Tile):
        self.__extend__(x, y)
        self.tiles[y][x] = tile
        tile.locX = x
        tile.locY = y

    def get_tile(self, x: int, y: int) -> Tile:
        self.__extend__(x, y)
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
