from Core.GameObject import *
from Core.GameStates.GameStates import *
import pygame

from Core.Physics.Collidable import *
from Game.Barrage.Barrage import *
from Game.Characters.Humans.Player import Player
from Game.Characters.Movable import *


class LandRobot(MovableEntity):
    __multiImage__: MultiImageSet

    @property
    def playerTarget(self) -> Player:
        return self.__scene__.player

    def __init__(self, start_pos: vec2, img: MultiImageSet, collide_anchor: vec2 = vec2(20, 48 - 24), size: vec2 = vec2(40, 96 - 24)):
        super().__init__()
        self.image = img
        self.__multiImage__ = img
        self.fractionLock = True
        self.gravity = 9.8

        self.size = size
        self.boundAnchor = collide_anchor
        self.centre = start_pos
        img.scale = 2.0
        self.physicSurfName = 'enemy'

    @property
    def front(self) -> Tile:
        area = self.areaRect
        tdec = int((area.top + 2) // TILE_LENGTH)
        bdec = int((area.bottom - 2) // TILE_LENGTH)
        if self.faceRight:
            pos_x = (area.i_right + 12) // TILE_LENGTH
        else:
            pos_x = (area.i_left - 12) // TILE_LENGTH

        tile = self.__tileMap__.get_tile(pos_x, tdec)
        for i in range(tdec + 1, bdec + 1):
            tmp = self.__tileMap__.get_tile(pos_x, i)
            if tmp.collidable:
                tile = tmp

        return tile

    @property
    def front_ground(self) -> Tile:
        area = self.areaRect
        bottom = area.i_bottom - 1
        if self.faceRight:
            pos_x = (area.i_right - 1) // TILE_LENGTH
        else:
            pos_x = (area.i_left + 1) // TILE_LENGTH
        pos_y = bottom // TILE_LENGTH
        return self.__tileMap__.get_tile(pos_x, pos_y)


class MeleeRobot(LandRobot):
    def __init__(self, pos: vec2):
        super().__init__(pos, MultiImageSet(vec2(32, 48), vec2(48, 48), 'Characters\\Enemys\\Robot1'))

    def update(self, args: GameArgs):
        if self.front.collidable or not self.front_ground.collidable:
            self.faceRight = self.image.flip

        self.set_move_intention(vec2(3, 0) if self.faceRight else vec2(-3, 0))

        if self.playerTarget