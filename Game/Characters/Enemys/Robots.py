from Core.GameObject import *
from Core.GameStates.GameState import *
import pygame

from Core.Physics.Collidable import *
from Game.Barrage.Barrage import *
from Game.Characters.Humans.Player import Player, PlayerBullet
from Game.Characters.Movable import *


class LandRobot(MovableEntity):
    __multiImage__: MultiImageSet

    @property
    def playerTarget(self) -> Player:
        return self.__scene__.player

    def __init__(self, start_pos: vec2, img: MultiImageSet, collide_anchor: vec2 = vec2(20, 48 - 24), size: vec2 = vec2(40, 96 - 24)):
        super().__init__()
        self.image = img
        self.gravity = 9.8
        self.__multiImage__ = img
        self.fractionLock = True
        self.gravity = 9.8

        self.size = size
        self.__boundAnchor__ = collide_anchor
        self.centre = start_pos
        img.scale = 2.0
        self.physicSurfName = 'enemy'

    @property
    def front(self) -> Tile:
        area = self.areaRect
        tdec = int((area.top + 2) // TILE_LENGTH)
        bdec = int((area.bottom - 12) // TILE_LENGTH)

        if self.faceRight:
            pos_x = (area.i_right + 12) // TILE_LENGTH
        else:
            pos_x = (area.i_left - 12) // TILE_LENGTH

        if bdec < 0:
            return Tile.Empty()

        tile = self.__tileMap__.get_tile(pos_x, bdec)
        for i in range(max(0, tdec), bdec):
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
        pos_y = (bottom - 5) // TILE_LENGTH
        return self.__tileMap__.get_tile(pos_x, pos_y + 1)

    def draw(self, render_args: RenderArgs):
        self.image.draw_self(render_args, self.centre)


class MeleeRobot(LandRobot):
    def __init__(self, *args):
        if len(args) == 1:
            pos = args[0]
        else:
            pos = vec2((TILE_LENGTH + 0.5) * args[0], TILE_LENGTH * args[1] - 48.0)
        super().__init__(pos, MultiImageSet(vec2(128, 128), vec2(128, 128), 'Characters\\Enemys\\Robot1'), vec2(30, 48), vec2(60, 192 - 52))
        self.image.scale = 1.45

    attacking: bool = False
    stage_timer: float = 0.0
    stage: int = 0
    attacked_timer: float = 0.0

    def on_collide(self, another):
        if not isinstance(another, PlayerBullet):
            raise Exception()
        self.attacked_timer = 0.1
        self.stage = 0
        self.attacking = False

    def update(self, args: GameArgs):
        fr = self.front
        if fr.collidable:
            self.faceRight = self.image.flip
        elif self.onGround:
            fr_g = self.front_ground
            if not fr_g.collidable:
                self.faceRight = self.image.flip

        if self.attacked_timer > 0:
            self.attacked_timer -= args.elapsedSec
            return

        if not self.attacking:
            self.set_move_intention(vec2(2, 0) if self.faceRight else vec2(-2, 0))
        self.move(args)

        dir_factor = 1 if self.faceRight else - 1
        d = (self.playerTarget.centre.x - self.centre.x) * dir_factor

        if 0 < d < 60:
            # in attack range:
            if not self.attacking:
                self.attacking = True
                self.stage_timer = 0.0
                self.stage = 0
        else:
            if self.attacking:
                self.attacking = False
                self.stage = 0
                self.stage_timer = 0.0

        self.stage_timer += args.elapsedSec

        if self.attacking:
            if self.stage_timer > 0.125:
                self.stage += 1
                self.stage_timer -= 0.125
                if self.stage == 3:
                    self.playerTarget.deal_damage()

                if self.stage == 4:
                    self.stage = 0
                    self.attacking = False

            self.__multiImage__.imageSource = self.__multiImage__.imageDict['Attack']

        else:
            if self.stage_timer > 0.125:
                self.stage += 1
                self.stage_timer -= 0.125

                if self.stage == 8:
                    self.stage = 0

            self.__multiImage__.imageSource = self.__multiImage__.imageDict['Walk']

        self.image.indexX = self.stage
