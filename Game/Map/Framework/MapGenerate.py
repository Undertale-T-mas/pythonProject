from enum import Enum

from Game.Map.Framework.MapObject import MapObject, ObjectInfo, ObjectLibrary, ObjectGenerate
from Game.Map.Framework.TileMap import TileMap
from Game.Map.Framework.Tiles import *


class TileGroup:
    corner_l: TileLibrary | None
    corner_r: TileLibrary | None
    top: TileLibrary | None
    left: TileLibrary | None
    right: TileLibrary | None
    bottom: TileLibrary | None
    inner: TileLibrary | None
    bottom_l: TileLibrary | None
    bottom_r: TileLibrary | None
    turn_tl: TileLibrary | None
    turn_tr: TileLibrary | None
    turn_bl: TileLibrary | None
    turn_br: TileLibrary | None

    def __init__(self,
                 corner_l: TileLibrary | None = None,
                 corner_r: TileLibrary | None = None,
                 top: TileLibrary | None = None,
                 left: TileLibrary | None = None,
                 right: TileLibrary | None = None,
                 bottom: TileLibrary | None = None,
                 inner: TileLibrary | None = None,
                 bottom_l: TileLibrary | None = None,
                 bottom_r: TileLibrary | None = None,
                 turn_tl: TileLibrary | None = None,
                 turn_tr: TileLibrary | None = None,
                 turn_bl: TileLibrary | None = None,
                 turn_br: TileLibrary | None = None
                 ):
        self.corner_r = corner_r
        self.corner_l = corner_l
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
        self.inner = inner
        self.bottom_l = bottom_l
        self.bottom_r = bottom_r
        self.turn_tr = turn_tr
        self.turn_tl = turn_tl
        self.turn_br = turn_br
        self.turn_bl = turn_bl

    def get_top(self):
        return self.top

    def get_corner_l(self):
        if self.corner_l is None:
            return self.get_top()
        return self.corner_l

    def get_corner_r(self):
        if self.corner_r is None:
            return self.get_top()
        return self.corner_r

    def get_inner(self):
        return self.inner

    def get_left(self):
        if self.left is None:
            return self.get_inner()
        return self.left

    def get_right(self):
        if self.right is None:
            return self.get_inner()
        return self.right

    def get_bottom(self):
        if self.bottom is None:
            return self.get_inner()
        return self.bottom

    def get_bottom_l(self):
        if self.bottom_l is None:
            return self.get_left()
        return self.bottom_l

    def get_bottom_r(self):
        if self.bottom_r is None:
            return self.get_right()
        return self.bottom_r

    def get_turn_tl(self):
        if self.turn_tl is None:
            return self.get_inner()
        return self.turn_tl

    def get_turn_tr(self):
        if self.turn_tr is None:
            return self.get_inner()
        return self.turn_tr

    def get_turn_bl(self):
        if self.turn_bl is None:
            return self.get_inner()
        return self.turn_bl

    def get_turn_br(self):
        if self.turn_br is None:
            return self.get_inner()
        return self.turn_br

    def get_by_state(self, top: bool, bottom: bool, left: bool, right: bool, tl: bool, tr: bool, bl: bool, br: bool):
        if not top:
            if left and right:
                return self.get_top()
            if left:
                return self.get_corner_r()
            if right:
                return self.get_corner_l()
            return self.get_top()
        else:
            if left and right:
                if bottom:
                    if not tl:
                        return self.get_turn_tl()
                    if not tr:
                        return self.get_turn_tr()
                    if not bl:
                        return self.get_turn_bl()
                    if not br:
                        return self.get_turn_br()
                    return self.get_inner()
                return self.get_bottom()
            if left:
                if not bottom:
                    return self.get_bottom_r()
                return self.get_right()
            if right:
                if not bottom:
                    return self.get_bottom_l()
                return self.get_left()
            if bottom:
                return self.get_bottom()
            return self.get_inner()


class FactoryIron(TileGroup):
    def __init__(self):
        super().__init__(
            TileLibrary.iron_cl,
            TileLibrary.iron_cr,
            TileLibrary.iron_t,
            TileLibrary.iron_l,
            TileLibrary.iron_r,
            bottom=TileLibrary.iron_b,
            inner=TileLibrary.iron_inner,
            bottom_l=TileLibrary.iron_bl,
            bottom_r=TileLibrary.iron_br,
            turn_tl=TileLibrary.iron_ttl,
            turn_tr=TileLibrary.iron_ttr,
            turn_bl=TileLibrary.iron_tbl,
            turn_br=TileLibrary.iron_tbr
        )


class FactoryWarn(TileGroup):
    def __init__(self):
        super().__init__(
            TileLibrary.warn_cl,
            TileLibrary.warn_cr,
            TileLibrary.warn_t,
            TileLibrary.warn_l,
            TileLibrary.warn_r,
            TileLibrary.warn_b,
            TileLibrary.purple_streak,
            TileLibrary.warn_bl,
            TileLibrary.warn_br,
            turn_tl=TileLibrary.warn_ttl,
            turn_tr=TileLibrary.warn_ttr,
            turn_bl=TileLibrary.warn_tbl,
            turn_br=TileLibrary.warn_tbr,
        )


class AutoTileMap(TileMap):
    all_data: Dict[str, Any]

    __l_exist__: bool
    __r_exist__: bool
    __t_exist__: bool
    __b_exist__: bool
    __tl__: bool
    __tr__: bool
    __bl__: bool
    __br__: bool

    _obj_id: int
    __tile_token__: Set[str]

    def __init__(self):
        super().__init__()
        self._obj_id = 0
        self.__tile_token__ = set()
        self.all_data = dict()

    def set_main(self, group: TileGroup):
        self.ins_group('m', group)
        self.ins_group('M', group)

    def ins_generator(self, token: str, func):
        self.all_data[token] = func

    def ins_save(self, token: str):
        self.ins_savable_obj(token, ArgAction(ObjectGenerate.make_crystal))

    def ins_tile(self, token: str, tile: TileInfo | TileLibrary, linkable: bool = True, back: bool = False):
        if isinstance(tile, TileLibrary):
            tile = tile.value

        def generator(x: int, y: int):
            if back:
                self.set_tile_back(x, y, Tile(tile))
            else:
                self.set_tile(x, y, Tile(tile))

        self.ins_generator(token, generator)
        if linkable:
            self.__tile_token__.add(token)

    def ins_enemy(self, token: str, enemy: type):
        if isinstance(enemy, Entity):
            enemy = type(enemy)

        def generator(x: int, y: int):
            self.add_object(enemy(x, y))

        self.ins_generator(token, generator)

    def ins_savable_obj(self, token: str, generate: ArgAction):
        def generator(x, y):
            self._obj_id += 1
            info = generate.act(self.__worldPos__, self._obj_id)
            self.add_object(MapObject(info, x, y))

        self.ins_generator(token, generator)

    def ins_obj(self, token: str, obj: ObjectInfo | ObjectLibrary):
        if isinstance(obj, ObjectLibrary):
            obj = obj.value

        def generator(x, y):
            self.add_object(MapObject(obj, x, y))

        self.ins_generator(token, generator)

    def is_tile(self, token: str) -> bool:
        return token in self.__tile_token__

    def ins_group(self, token: str, group: TileGroup):
        def generator(x, y):
            self.set_tile(x, y, Tile(group.get_by_state(
                self.__t_exist__,
                self.__b_exist__,
                self.__l_exist__,
                self.__r_exist__,
                self.__tl__,
                self.__tr__,
                self.__bl__,
                self.__br__
            )))

        self.__tile_token__.add(token)
        self.ins_generator(token, generator)

    def generate(self, tiles: List[List[str]]):

        self.height = len(tiles)
        self.width = len(tiles[0])

        for y in range(self.height):
            for x in range(self.width):

                if tiles[y][x] == '0' or tiles[y][x] == '':
                    continue

                if x == 0:
                    l = True
                else:
                    l = self.is_tile(tiles[y][x - 1])
                if x == self.width - 1:
                    r = True
                else:
                    r = self.is_tile(tiles[y][x + 1])

                if y == 0:
                    t = True
                    tl = True
                    tr = True
                else:
                    t = self.is_tile(tiles[y - 1][x])
                    if x == 0:
                        tl = True
                    else:
                        tl = self.is_tile(tiles[y - 1][x - 1])
                    if x == self.width - 1:
                        tr = True
                    else:
                        tr = self.is_tile(tiles[y - 1][x + 1])

                if y == self.height - 1:
                    b = True
                    bl = True
                    br = True
                else:
                    b = self.is_tile(tiles[y + 1][x])
                    if x == 0:
                        bl = True
                    else:
                        bl = self.is_tile(tiles[y + 1][x - 1])
                    if x == self.width - 1:
                        br = True
                    else:
                        br = self.is_tile(tiles[y + 1][x + 1])

                self.__l_exist__ = l
                self.__r_exist__ = r
                self.__t_exist__ = t
                self.__b_exist__ = b
                self.__tl__ = tl
                self.__tr__ = tr
                self.__bl__ = bl
                self.__br__ = br

                _all = tiles[y][x].split(',')
                for u in _all:
                    self.all_data[u](x, y)
