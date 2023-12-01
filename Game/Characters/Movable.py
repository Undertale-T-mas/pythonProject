from Game.Map.FightScene import *
from Game.Map.Framework.TileMap import *
from Game.Map.Framework.Tiles import *
from Core.GameStates.GameStates import *
from pygame import Vector2 as vec2


class MovableEntity(Entity, Collidable):
    __tileMap__: TileMap

    def __init__(self):
        s = current_scene()

        if not isinstance(s, FightScene):
            raise Exception()

        self.__tileMap__ = s.tileMap
        self.physicArea = CollideRect()

    __moveIntention__: vec2 = vec2(0, 0)
    __jumpIntention__: bool = False

    __onGround__: bool = False

    __boundAnchor__: vec2 | None = None
    __ySpeed__: float = 0.0
    __gravity__: float = 0.0
    __collision__: bool = True

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

    def __check_on_ground__(self) -> bool:
        if not isinstance(self.physicArea, CollideRect):
            raise Exception()
        if self.__ySpeed__ < 0.0:
            self.__onGround__ = False
            return False

        bdec = self.physicArea.area.bottom // TILE_LENGTH
        ldec = self.physicArea.area.left // TILE_LENGTH
        rdec = self.physicArea.area.right // TILE_LENGTH

        for xdec in range(ldec, rdec + 1):
            tile = self.__tileMap__.get_tile(xdec, bdec)
            if tile.uuid != 0:
                if not isinstance(tile.physicArea, CollideRect):
                    raise Exception()

                r = tile.physicArea.area

                if r.top < self.physicArea.area.bottom + 0.001:
                    last_y = self.physicArea.area.bottom - self.__ySpeed__
                    if last_y - r.top > TILE_LENGTH / 3.2:
                        return False
                    self.__onGround__ = True
                    self.__inGroundDistance__ = self.physicArea.area.bottom - r.top
                    return True

        self.__onGround__ = (self.physicArea.area.bottom > 450)
        if self.__onGround__:
            self.__inGroundDistance__ = self.physicArea.area.bottom - 450
        return self.__onGround__

    def jump(self, speed: float):
        self.__jumpIntention__ = True
        self.__ySpeed__ = -speed

    def set_move_intention(self, move_intention: vec2):
        self.__moveIntention__ = move_intention

    def move(self, args: GameArgs) -> vec2:
        if not isinstance(self.physicArea, CollideRect):
            raise Exception()

        old_pos = self.centre
        move_del = self.__moveIntention__ * args.elapsedSec * 60

        # we check the gravity in the following codes:
        self.centre = old_pos + move_del
        self.physicArea.area = Rect(self.centre - self.boundAnchor, self.size)

        if self.__gravity__ > 0.001:
            self.__check_on_ground__()

            if self.onGround:
                self.__ySpeed__ = 0.0
                move_del.y -= self.__inGroundDistance__
            else:
                self.__ySpeed__ += self.__gravity__ * args.elapsedSec * 2.0

            move_del.y += self.__ySpeed__ * args.elapsedSec * 60

        # we check the body collision in the following codes:
        self.centre = old_pos + move_del
        self.physicArea.area = Rect(self.centre - self.boundAnchor, self.size)

        if self.__collision__:
            bdec = int((self.physicArea.area.bottom - 5) // TILE_LENGTH)
            t_del = 2
            f_mode = False
            if self.__ySpeed__ < -1:
                t_del = -2
                f_mode = True
            tdec = int((self.physicArea.area.top + t_del) // TILE_LENGTH)
            ldec = self.physicArea.area.left // TILE_LENGTH
            rdec = self.physicArea.area.right // TILE_LENGTH

            if bdec >= 0 and tdec >= 0 and ldec >= 0 and rdec >= 0:
                # check left and right:
                if abs(move_del.x) > 1e-5 or f_mode:
                    l = self.physicArea.area.left
                    r = self.physicArea.area.right

                    for ydec in range(tdec, bdec + 1):
                        tile = self.__tileMap__.get_tile(ldec, ydec)
                        if tile.uuid == 0:
                            continue
                        if tile.areaRect.right + 0.0001 > l:
                            dx = tile.areaRect.right - l + 0.0001
                            if dx < TILE_LENGTH * 0.3:
                                move_del.x += dx
                                self.centre.x += dx
                                self.physicArea.area = self.physicArea.area.move(dx, 0)

                    for ydec in range(tdec, bdec + 1):
                        tile = self.__tileMap__.get_tile(rdec, ydec)
                        if tile.uuid == 0:
                            continue
                        if tile.areaRect.left - 0.0001 < r:
                            dx = max(1.0111, r - tile.areaRect.left + 1.1111)
                            if dx < TILE_LENGTH * 0.3:
                                move_del.x -= dx
                                self.centre.x -= dx
                                self.physicArea.area = self.physicArea.area.move(-dx, 0)

                bdec = self.physicArea.area.bottom // TILE_LENGTH
                tdec = self.physicArea.area.top // TILE_LENGTH
                ldec = self.physicArea.area.left // TILE_LENGTH
                rdec = self.physicArea.area.right // TILE_LENGTH

                if bdec >= 0 and tdec >= 0 and ldec >= 0 and rdec >= 0 and self.__ySpeed__ <= 0:
                    # check the head
                    head_y = self.centre.y - self.boundAnchor.y
                    for i in range(ldec, rdec + 1):
                        tile = self.__tileMap__.get_tile(i, tdec)
                        if tile.uuid == 0:
                            continue
                        if tile.areaRect.bottom + 0.001 > head_y:
                            move_del.y += tile.areaRect.bottom - head_y
                            if self.__ySpeed__ < 0:
                                self.__ySpeed__ = 0

        np = old_pos + move_del
        self.centre = np
        self.physicArea.area = Rect(self.centre - self.boundAnchor, self.size)

        self.__moveIntention__ = vec2(0, 0)

        return move_del
