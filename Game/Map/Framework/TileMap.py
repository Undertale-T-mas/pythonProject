from Game.Map.Framework.TileBack import *
from Game.Map.Framework.Tiles import *
from typing import *

from Game.Map.Framework.WorldData import WorldData


class TileMap(Entity):
    in_initialize: bool = False
    overlay_image: Texture | None
    bgm: str
    savable: bool
    player_controllable: bool
    overlay_intensity: float
    overlay_pos: vec2

    __worldPos__: vec2
    __backs__: Set[Tile]
    __backupd__: Set[Tile]

    @property
    def worldPos(self):
        return self.__worldPos__

    @worldPos.setter
    def worldPos(self, val: vec2):
        self.__worldPos__ = val
        WorldData.insert(self, int(self.__worldPos__.x), int(self.__worldPos__.y))

    __objects__: List[GameObject]

    def get_objects(self):
        return self.__objects__

    tiles: List[List[Tile]]

    __width__: int
    __height__: int
    width: int
    height: int

    tileChanged: bool

    actived: List[Set[int]]
    updatable: List[Set[int]]
    args_tmp: GameArgs

    __backGrounds__: List[Entity]
    __initialized__: bool

    def add_object(self, obj: GameObject):
        self.__objects__.append(obj)

    def __init__(self):
        super().__init__()
        self.overlay_intensity = 0.25
        self.overlay_pos = vec2(0.0, 0.0)
        self.bgm = ''
        self.savable = True
        self.overlay_image = None
        self.__objects__ = []
        self.surfaceName = 'bg'
        self.__backupd__ = set()
        self.__initialized__ = False
        self.actived = []
        self.updatable = []
        self.__backs__ = set()
        self.__width__ = 0
        self.tiles = []
        self.__backGrounds__ = []
        self.__height__ = 0
        self.tileChanged = True
        self.width = 0
        self.height = 0
        self.player_controllable = True

    def add_background(self, path: str, factor_x: float, alpha: float = 1.0):
        img = SingleImage('BackGrounds\\' + path)
        img.alpha = alpha
        self.__backGrounds__.append(TileBack(factor_x, img, alpha))

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

    def set_tile_back(self, x: int, y: int, tile: Tile):
        tile.locX = x
        tile.locY = y
        tile.set_back()
        self.width = max(self.width, x + 1)
        self.height = max(self.height, y + 1)
        self.tileChanged = True
        if tile.info.onUpdate is not None:
            self.__backupd__.add(tile)
        self.__backs__.add(tile)

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
            for i in self.__backs__:
                i.update(args)

        for obj in self.__backupd__:
            obj.update(args)

        for obj in self.__backGrounds__:
            obj.update(args)

    def draw(self, args: RenderArgs):
        for obj in self.__backGrounds__:
            obj.draw(args)

        for obj in self.__backs__:
            obj.draw(args)

        if args.quality <= 111:
            self.tileChanged = False
        y = -1
        for i in self.tiles:
            y += 1
            for j in self.actived[y]:
                i[j].draw(args)

    pass
