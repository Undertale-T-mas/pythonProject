from Game.Map.Framework.TileBack import *
from Game.Map.Framework.Tiles import *
from typing import *


class TileMap(Entity):
    worldPos: vec2
    tiles: List[List[Tile]]

    __width__: int
    __height__: int
    width: int
    height: int

    tileChanged: bool

    actived: List[Set[int]]
    updatable: List[Set[int]]

    __backGrounds__: List[Entity]
    __initialized__: bool

    def __init__(self):
        super().__init__()
        self.surfaceName = 'bg'
        self.__initialized__ = False
        self.actived = []
        self.updatable = []
        self.__width__ = 0
        self.tiles = []
        self.__backGrounds__ = []
        self.__height__ = 0
        self.tileChanged = True
        self.width = 0
        self.height = 0

    def add_background(self, path: str, factor_x: float, alpha: float = 1.0):
        img = SingleImage('BackGrounds\\' + path)
        img.alpha = alpha
        self.__backGrounds__.append(TileBack(factor_x, img))

    def __extend__(self, x: int, y: int):
        while y >= self.__height__:
            self.__height__ += 1
            row = []
            for i in range(self.__width__):
                row.append(Tile(TileLibrary.empty))
            self.tiles.append(row)
            self.actived.append(set())
            self.updatable.append(set())

        if x >= self.__width__:
            for y in range(self.__height__):
                for i in range(x - self.__width__ + 1):
                    self.tiles[y].append(Tile(TileLibrary.empty))
            self.__width__ = x

    def set_tile(self, x: int, y: int, tile: Tile):
        self.__extend__(x, y)
        self.tiles[y][x] = tile
        tile.locX = x
        tile.locY = y
        self.width = max(self.width, x + 1)
        self.height = max(self.height, y + 1)
        if x not in self.actived[y]:
            self.actived[y].add(x)
        if tile.info.onUpdate is not None:
            if x not in self.updatable[y]:
                self.updatable[y].add(x)
        self.tileChanged = True

    def get_tile(self, x: int, y: int) -> Tile:
        self.__extend__(x, y)
        return self.tiles[y][x]

    def update(self, args: GameArgs):
        y = -1
        if self.__initialized__:
            for i in self.tiles:
                y += 1
                for j in self.updatable[y]:
                    i[j].update(args)
        else:
            self.__initialized__ = True
            for i in self.tiles:
                y += 1
                for j in self.actived[y]:
                    i[j].update(args)

        for obj in self.__backGrounds__:
            obj.update(args)

    def draw(self, args: RenderArgs):
        for obj in self.__backGrounds__:
            obj.draw(args)

        if args.quality <= MED_QUALITY:
            self.tileChanged = False
        y = -1
        for i in self.tiles:
            y += 1
            for j in self.actived[y]:
                i[j].draw(args)

    pass
