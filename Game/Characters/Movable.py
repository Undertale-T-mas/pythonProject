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

    __ySpeed__: float = 0.0
    __gravity__: float = 0.0

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
    def size(self) -> vec2:
        if not isinstance(self.physicArea, CollideRect):
            raise Exception()
        return self.physicArea.area.size

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
        self.__onGround__ = (self.physicArea.area.bottom > 450)
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
        move_del = self.__moveIntention__
        self.centre = old_pos + move_del

        if self.__gravity__ > 0.001:
            self.__check_on_ground__()

            if self.onGround:
                self.__ySpeed__ = 0.0
                move_del.y -= self.__inGroundDistance__
            else:
                self.__ySpeed__ += self.__gravity__ * args.elapsedSec * 2

            move_del.y += self.__ySpeed__

        np = old_pos + move_del
        self.centre = np
        self.physicArea.area.center = np

        self.__moveIntention__ = vec2(0, 0)

        return move_del
