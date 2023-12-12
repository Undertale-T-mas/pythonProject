from Core.Animation.Animation import *
from Resources.ResourceLib import *
from Core.GameObject import *
from Core.GameStates.GameState import *
import pygame

from Core.Physics.Collidable import *
from Game.Barrage.Barrage import *
from Game.Characters.Humans.Player import Player, PlayerBullet
from Game.Characters.Movable import *


class RobotBullet(Barrage):
    rect: CollideRect

    def __init__(self, path: str, start: vec2, flip: bool, speed: vec2, damage: Damage):
        super().__init__(damage)
        self.image = SingleImage(path)
        self.move(EasingGenerator.linear(start, speed))
        self.image.scale = 2
        self.image.flip = flip
        self.autoDispose = True
        self.physicSurfName = 'barrage'
        self.rect = CollideRect()
        img_sz = self.image.imageSource.get_size()
        self.rect.area = FRect(0, 0, max(1, img_sz[0] - 7), max(1, img_sz[1] - 7))
        self.physicArea = self.rect

    def update(self, args: GameArgs):
        self.rect.area.centre = self.centre
        super().update(args)

    def draw(self, render_args: RenderArgs):
        self.image.draw_self(render_args, self.centre)

    def on_collide(self, another):
        super().on_collide(another)


class LandRobot(MovableEntity):
    __multiImage__: MultiImageSet
    __hp__: float
    __defense__: int

    @property
    def playerTarget(self) -> Player:
        return self.__scene__.player

    def __init__(self, start_pos: vec2, img: MultiImageSet, collide_anchor: vec2 = vec2(20, 48 - 24), size: vec2 = vec2(40, 96 - 24)):
        super().__init__()
        self.image = img
        self.__hp__ = 30.0
        self.__defense__ = 0
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

    def on_collide(self, another):
        Sounds.robot_damaged.play()

    def deal_damage(self, damage_level: int):
        self.__hp__ -= Math.damage(damage_level, self.__defense__)
        if self.__hp__ <= 0:
            self.died()

    def update(self, args: GameArgs):
        if not self.__initialized__:
            self.__start__()


class MeleeRobot(LandRobot):
    def __init__(self, *args):
        if len(args) == 1:
            pos = args[0]
        else:
            pos = vec2((TILE_LENGTH + 0.5) * args[0], TILE_LENGTH * args[1] - 48.0)

        super().__init__(
            pos,
            MultiImageSet(vec2(128, 128), vec2(128, 128), 'Characters\\Enemys\\Robot1'),
            vec2(30, 48 - 20), vec2(60, 192 - 52 - 20)
        )
        self.__killed__ = False
        self.image.scale = 1.45
        self.attacking = False
        self.stage_timer = 0.0
        self.stage = 0
        self.attacked_timer = 0.0

    attacking: bool
    stage_timer: float
    stage: int
    attacked_timer: float

    def on_collide(self, another):
        if not isinstance(another, PlayerBullet):
            raise Exception()
        super().on_collide(another)
        self.attacked_timer = 0.1
        self.stage = 0
        self.attacking = False
        if another.centre.x < self.centre.x:
            self.give_force(5)
        else:
            self.give_force(-5)
        self.jump(1)
        self.deal_damage(another.damage.damageLevel)

    __killed__: bool

    def died(self):
        self.__killed__ = True
        img = self.__multiImage__
        img.imageSource = img.imageDict['Dead']
        img.indexX = 0
        instance_create(AlphaAnimation(img, 0.12, self.centre, 0.04))
        instance_create(DelayedAction(0.04, Action(Sounds.robot_died.play)))

    def update(self, args: GameArgs):
        super().update(args)

        if self.__killed__:
            self.dispose()
            return
        fr = self.front
        if fr.collidable:
            self.faceRight = self.image.flip
        elif self.onGround:
            fr_g = self.front_ground
            if not fr_g.collidable:
                self.faceRight = self.image.flip

        if not self.attacking:
            self.set_move_intention(vec2(2, 0) if self.faceRight else vec2(-2, 0))

        self.move(args)

        if self.attacked_timer > 0:
            self.attacked_timer -= args.elapsedSec
            return

        dir_factor = 1 if self.faceRight else - 1
        d = (self.playerTarget.centre.x - self.centre.x) * dir_factor
        h = (self.playerTarget.centre.y - self.centre.y)

        if 0 < d < 65 and -40 < h < 85:
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
                    self.playerTarget.deal_damage(Damage(self, 1))

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


class GunRobot(LandRobot):
    __shootInterval__: float

    def __init__(self, *args):
        self.shoot_interval = 2.0
        if len(args) == 1:
            pos = args[0]
        else:
            pos = vec2((TILE_LENGTH + 0.5) * args[0], TILE_LENGTH * args[1] - 48.0)

        super().__init__(
            pos,
            MultiImageSet(vec2(64, 96), vec2(96, 96), 'Characters\\Enemys\\Robot2'),
            vec2(30, 48 - 20), vec2(60, 192 - 20 - 41)
        )
        self.__killed__ = False
        self.image.scale = 1.45 * 1.5
        self.attacking = False
        self.stage_timer = 0.0
        self.stage = 0
        self.attacked_timer = 0.0
        self.attack_timer = self.shoot_interval

    @property
    def shoot_interval(self):
        return self.__shootInterval__

    @shoot_interval.setter
    def shoot_interval(self, val: float):
        self.__shootInterval__ = val

    attacking: bool
    stage_timer: float
    stage: int
    attacked_timer: float
    attack_timer: float

    def on_collide(self, another):
        if not isinstance(another, PlayerBullet):
            raise Exception()
        super().on_collide(another)
        self.attacked_timer = 0.1
        self.stage = 0
        self.attacking = False
        if another.centre.x < self.centre.x:
            self.give_force(5)
        else:
            self.give_force(-5)
        self.jump(1)
        self.deal_damage(another.damage.damageLevel)

    __killed__: bool

    def died(self):
        self.__killed__ = True
        img = self.__multiImage__
        img.imageSource = img.imageDict['Death']
        img.indexX = 0
        instance_create(AlphaAnimation(img, 0.12, self.centre, 0.04))
        instance_create(DelayedAction(0.04, Action(Sounds.robot_died.play)))

    def attack(self):
        d = vec2(-50, 24) if self.image.flip else vec2(50, 24)
        instance_create(RobotBullet(
            'Objects\\Barrage\\Robot2_bullet.png', self.centre + d,
            self.image.flip,
            vec2(-800, 0) if self.image.flip else vec2(800, 0),
            Damage(self, 1)
        ))

    def update(self, args: GameArgs):
        super().update(args)

        if self.__killed__:
            self.dispose()
            return
        fr = self.front
        if fr.collidable:
            self.faceRight = self.image.flip
        elif self.onGround:
            fr_g = self.front_ground
            if not fr_g.collidable:
                self.faceRight = self.image.flip

        if not self.attacking:
            self.set_move_intention(vec2(2, 0) if self.faceRight else vec2(-2, 0))

        self.move(args)

        if self.attacked_timer > 0:
            self.attacked_timer -= args.elapsedSec
            return

        dir_factor = 1 if self.faceRight else - 1
        d = (self.playerTarget.centre.x - self.centre.x) * dir_factor
        h = (self.playerTarget.centre.y - self.centre.y)

        self.stage_timer += args.elapsedSec
        self.attack_timer -= args.elapsedSec
        if self.attack_timer <= 0:
            self.attacking = True
            self.attack_timer += self.shoot_interval
            self.stage = 0

        if self.attacking:
            if self.stage_timer > 0.125:
                self.stage += 1
                self.stage_timer -= 0.125
                if self.stage == 3:
                    self.attack()

                if self.stage == 6:
                    self.stage = 0
                    self.attacking = False

            self.__multiImage__.imageSource = self.__multiImage__.imageDict['Attack']

        else:
            if self.stage_timer > 0.125:
                self.stage += 1
                self.stage_timer -= 0.125

                if self.stage == 6:
                    self.stage = 0

            self.__multiImage__.imageSource = self.__multiImage__.imageDict['Walk']

        self.image.indexX = self.stage
