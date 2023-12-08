from Game.Map.Framework.Tiles import *
from typing import *


class TileMap(Entity):
    worldPos: vec2
    tiles: List[List[Tile]] = []

    width: int = 0
    height: int = 0

    actived: List[Set[int]]

    def __init__(self):
        self.surfaceName = 'bg'
        self.actived = []

    def __extend__(self, x: int, y: int):
        while y >= self.height:
            self.height += 1
            row = []
            for i in range(self.width):
                row.append(Tile(TileLibrary.empty))
            self.tiles.append(row)
            self.actived.append(set())

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
        if x not in self.actived[y]:
            self.actived[y].add(x)

    def get_tile(self, x: int, y: int) -> Tile:
        self.__extend__(x, y)
        return self.tiles[y][x]

    def update(self, args: GameArgs):
        y = -1
        for i in self.tiles:
            y += 1
            for j in self.actived[y]:
                i[j].update(args)

    def draw(self, args: RenderArgs):
        y = -1
        for i in self.tiles:
            y += 1
            for j in self.actived[y]:
                i[j].draw(args)

    pass
