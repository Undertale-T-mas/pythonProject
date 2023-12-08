from Game.Scenes.TileMapScene import TileMapScene
from Game.Map.Framework.TileMap import *
from Game.Map.Framework.Tiles import *
from Core.GameStates.GameState import *
from pygame import Vector2 as vec2


class MovableEntity(Entity, Collidable):
    __tileMap__: TileMap
    __scene__: TileMapScene

    def __init__(self):
        self.physicSurfName = 'enemy'
        self.__lastMove__ = self.__moveIntention__ = vec2(0, 0)
        s = current_scene()

        if not isinstance(s, TileMapScene):
            raise Exception()

        self.__scene__ = s
        self.__tileMap__ = s.tileMap
        self.physicArea = CollideRect()

    def died(self):
        self.dispose()

    @property
    def faceRight(self) -> bool:
        return not self.image.flip

    @faceRight.setter
    def faceRight(self, val: bool):
        self.image.flip = not val

    @property
    def areaRect(self) -> FRect:
        if not isinstance(self.physicArea, CollideRect):
            raise Exception()
        return self.physicArea.area

    __moveIntention__: vec2
    __jumpIntention__: bool = False
    __groundTile__: Tile | None = None
    __fractionLock__: bool = False

    __onGround__: bool = False

    __boundAnchor__: vec2 | None = None
    __ySpeed__: float = 0.0
    __gravity__: float = 0.0
    __collision__: bool = True

    @property
    def fractionLock(self) -> bool:
        return self.__fractionLock__

    @fractionLock.setter
    def fractionLock(self, val: bool):
        self.__fractionLock__ = False

    @property
    def boundAnchor(self) -> vec2:
        if self.__boundAnchor__ is not None:
            return self.__boundAnchor__
        return self.size / 2

    @boundAnchor.setter
    def boundAnchor(self, anchor: vec2):
        self.__boundAnchor__ = anchor

    @property
    def gravity(self) -> float:
        return self.__gravity__

    @gravity.setter
    def gravity(self, gravity: float):
        self.__gravity__ = gravity

    @property
    def onGround(self) -> bool:
        return self.__onGround__

    @property
    def collidable(self) -> bool:
        return self.__collision__

    @collidable.setter
    def collidable(self, state: bool):
        self.__collision__ = state

    @property
    def size(self) -> vec2:
        if not isinstance(self.physicArea, CollideRect):
            raise Exception()
        return vec2(self.physicArea.area.size)

    @size.setter
    def size(self, size: vec2):
        if not isinstance(self.physicArea, CollideRect):
            raise Exception()
        self.physicArea.area.size = size

    __inGroundDistance__ = 0.0

    def __check_on_ground__(self, l_limit, r_limit) -> bool:
        self.__groundTile__ = None
        if not isinstance(self.physicArea, CollideRect):
            raise Exception()
        if self.__ySpeed__ < 0.0:
            self.__onGround__ = False
            return False

        l_limit += 3
        r_limit -= 3

        bdec = self.physicArea.area.i_bottom // TILE_LENGTH
        ldec = self.physicArea.area.i_left // TILE_LENGTH
        rdec = self.physicArea.area.i_right // TILE_LENGTH
        xpos = int(self.centre.x) // TILE_LENGTH

        order = [xpos]

        for i in range(ldec, rdec + 1):
            if i == xpos:
                continue
            order.append(i)

        for xdec in order:
            tile = self.__tileMap__.get_tile(xdec, bdec)
            if tile.uuid != 0:
                if not isinstance(tile.physicArea, CollideRect):
                    raise Exception()
                if not tile.collidable:
                    continue

                if r_limit <= tile.areaRect.left:
                    continue
                if l_limit >= tile.areaRect.right:
                    continue

                r = tile.physicArea.area

                if r.top < self.physicArea.area.bottom + 0.001:
                    last_y = self.physicArea.area.bottom - self.__ySpeed__
                    if last_y - r.top > TILE_LENGTH / 3.2:
                        self.__onGround__ = False
                        return False
                    self.__onGround__ = True
                    self.__inGroundDistance__ = self.physicArea.area.bottom - r.top
                    self.__groundTile__ = tile
                    return True

        self.__onGround__ = (self.physicArea.area.bottom > 450)
        if self.__onGround__:
            self.__inGroundDistance__ = self.physicArea.area.bottom - 450
        return self.__onGround__

    def jump(self, speed: float):
        self.__jumpIntention__ = True
        self.__ySpeed__ = -speed * 1.2

    def set_move_intention(self, move_intention: vec2):
        self.__moveIntention__ = move_intention

    __lastMove__: vec2

    def move(self, args: GameArgs) -> vec2:
        if not isinstance(self.physicArea, CollideRect):
            raise Exception()

        old_pos = self.centre
        move_del = self.__moveIntention__ * args.elapsedSec * 60
        old_move_del = vec2(move_del.x, move_del.y)

        if not self.__fractionLock__:
            ground_tile = self.__groundTile__
            if ground_tile is None:
                fr = 0.2
            else:
                fr = ground_tile.fraction

            lerps = min(args.elapsedSec * 60 * fr, 1)
            x_intention_speed = self.__moveIntention__.x * args.elapsedSec * 60
            move_del.x = self.__lastMove__.x * (1 - lerps) + x_intention_speed * lerps
            if abs(move_del.x) < 0.1:
                move_del.x = 0

        self.centre = old_pos + move_del
        last_area = self.physicArea.area
        self.physicArea.area = FRect(self.centre - self.boundAnchor, self.size)

        # we check the gravity in the following codes:

        if self.__gravity__ > 0.001:
            self.__check_on_ground__(
                max(last_area.left, self.physicArea.area.left),
                min(last_area.right, self.physicArea.area.right)
            )

            if self.onGround:
                self.__ySpeed__ = 0.0
                move_del.y -= self.__inGroundDistance__
            else:
                self.__ySpeed__ += self.__gravity__ * args.elapsedSec * 2.86

            move_del.y += self.__ySpeed__ * args.elapsedSec * 60

        # we check the body collision in the following codes:
        self.centre = old_pos + move_del
        self.physicArea.area = FRect(self.centre - self.boundAnchor, self.size)

        if self.__collision__:
            bdec = int((self.physicArea.area.bottom - 5) // TILE_LENGTH)
            t_del = 2
            f_mode = False
            if self.__ySpeed__ <= 0:
                t_del = -2
                f_mode = True
            tdec = int((self.physicArea.area.top + t_del) // TILE_LENGTH)
            ldec = self.physicArea.area.i_left // TILE_LENGTH
            rdec = self.physicArea.area.i_right // TILE_LENGTH

            if bdec >= 0 and tdec >= 0 and ldec >= 0 and rdec >= 0:
                # check left and right:
                if abs(move_del.x) > 1e-5 or f_mode:
                    l = self.physicArea.area.left
                    r = self.physicArea.area.right

                    dx = 0

                    for ydec in range(tdec, bdec + 1):
                        tile = self.__tileMap__.get_tile(ldec, ydec)
                        if tile.uuid == 0:
                            continue
                        if not tile.collidable:
                            continue
                        if tile.areaRect.right + 0.00001 > l:
                            tmp_dx = tile.areaRect.right - l
                            if tmp_dx < TILE_LENGTH * 0.3:
                                dx = max(dx, tmp_dx)

                    if dx > 0:
                        move_del.x += dx
                        self.centre.x += dx
                        self.physicArea.area = self.physicArea.area.move(dx, 0)
                        dx = 0

                    for ydec in range(tdec, bdec + 1):
                        tile = self.__tileMap__.get_tile(rdec, ydec)
                        if tile.uuid == 0:
                            continue
                        if not tile.collidable:
                            continue
                        if tile.areaRect.left - 0.00001 < r:
                            tmp_dx = r - tile.areaRect.left
                            if tmp_dx < TILE_LENGTH * 0.3:
                                dx = max(dx, tmp_dx)

                    if dx > 0:
                        move_del.x -= dx
                        self.centre.x -= dx
                        self.physicArea.area = self.physicArea.area.move(-dx, 0)

                bdec = self.physicArea.area.i_bottom // TILE_LENGTH
                tdec = self.physicArea.area.i_top // TILE_LENGTH
                ldec = self.physicArea.area.i_left // TILE_LENGTH
                rdec = self.physicArea.area.i_right // TILE_LENGTH

                if bdec >= 0 and tdec >= 0 and ldec >= 0 and rdec >= 0 and self.__ySpeed__ <= 0:
                    # check the head
                    head_y = self.centre.y - self.boundAnchor.y
                    for i in range(ldec, rdec + 1):
                        tile = self.__tileMap__.get_tile(i, tdec)
                        if tile.uuid == 0:
                            continue
                        if not tile.collidable:
                            continue
                        if self.physicArea.area.right <= tile.areaRect.left:
                            continue
                        if self.physicArea.area.left >= tile.areaRect.right:
                            continue
                        if tile.areaRect.bottom + 0.001 > head_y:
                            move_del.y += tile.areaRect.bottom - head_y
                            if self.__ySpeed__ < 0:
                                self.__ySpeed__ = 0

        np = old_pos + move_del
        self.centre = np
        self.physicArea.area = FRect(self.centre - self.boundAnchor, self.size)

        self.__moveIntention__ = vec2(0, 0)
        self.__lastMove__ = old_move_del

        return move_del
