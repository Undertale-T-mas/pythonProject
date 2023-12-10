import Resources.ResourceLib
from Core.Animation.Animation import *
from Core.GameObject import *
from Core.GameStates.GameState import *
import pygame

from Core.Physics.Collidable import *
from Game.Barrage.Barrage import *
from Game.Characters.Humans.HPBar import HPBar
from Game.Characters.Movable import *
from Game.Tech.DataLib import TechData
from Resources.ResourceLib import *


class MoveState(Enum):
    idle = 0,
    run = 1,
    jump = 2,


class PlayerBullet(Barrage):
    rect: CollideRect

    def __init__(self, start: vec2, d: bool, damage: Damage):
        super().__init__(damage)
        self.image = MultiImage('Characters\\Player\\Bullets')
        self.physicSurfName = 'pl_bullet'
        self.move(EasingGenerator.linear(start, vec2(-1100, 0) if d else vec2(1100, 0)))
        self.image.scale = 2
        self.image.flip = d
        self.autoDispose = True
        self.rect = CollideRect()
        self.rect.area = FRect(0, 0, 1, 3)
        self.physicArea = self.rect

    def update(self, args: GameArgs):
        self.rect.area.centre = self.centre
        super().update(args)
        pass

    def draw(self, render_args: RenderArgs):
        self.image.draw_self(render_args, self.centre)

    def on_collide(self, another):
        super().on_collide(another)
        img = ImageSet(
                vec2(48, 48),
                vec2(48, 48),
                'Effects\\Sparks\\' + str(Math.rand(0, 2)) + '.png'
              )
        img.scale = 1.5
        instance_create(Animation(
            img,
            0.05,
            self.centre
        ))


class Weapon(Entity):
    def __init__(self):
        super().__init__()
        self.image = MultiImage('Characters\\Player\\Weapons')
        self.image.scale = 2

    def update(self, args: GameArgs):
        super().update(args)
        self.idx = 0
        self.image.imageSource = self.image.imageList[0]

    def draw(self, render_args: RenderArgs):
        self.image.draw_self(render_args, self.centre)

    def shoot(self, damage: Damage):
        d = self.delta[self.idx]
        if self.image.flip:
            d = vec2(-d.x, d.y)
        instance_create(PlayerBullet(self.centre + d, self.image.flip, damage))

    idx = 0
    delta: List[vec2] = [
        vec2(20, -2)
    ]


class MoveSmoke(Entity):
    speedX: float

    def __init__(self, place: vec2, speed_x: float, path: str, index_max: int = 4):
        super().__init__()
        self.image = ImageSet(vec2(48, 48), vec2(48, 48), path)
        self.image.scale = 1.5
        self.tot = 0
        self.speedX = speed_x
        self.centre = place
        self.image.alpha = 0.85
        self.indexMax = index_max

    tot: float
    indexMax: int

    def update(self, args: GameArgs):
        self.tot += args.elapsedSec
        self.image.alpha -= args.elapsedSec
        self.centre.x += self.speedX * args.elapsedSec * 1.5
        if self.tot > 0.08:
            self.tot -= 0.08
            self.image.indexX += 1
            if self.image.indexX == self.indexMax:
                self.dispose()


class PlayerHand(Entity):
    def __init__(self, follow):
        self.__follow__ = follow
        self.image = MultiImage('Characters\\Player\\Hands')
        self.image.scale = 2
        self.__weapon__ = Weapon()

    __weapon__: Weapon
    __follow__: Entity
    __state__: MoveState
    visible: bool = True
    phase: int = 0
    idx: int = 1
    __inAttack__: bool = False

    __runPos__: List[vec2] = [
        vec2(7, 7),
        vec2(7, 7),
        vec2(7, 7),
        vec2(7, 7),
        vec2(7, 7),
        vec2(7, 7),
        vec2(7, 7)
    ]
    __jumpPos__: List[vec2] = [
        vec2(12, 4),
        vec2(12, 1),
        vec2(12, -3),
        vec2(12, 3)
    ]
    __weaponMove__: List[vec2] = [
        vec2(0, 9),
        vec2(7, 6),
        vec2(9, 0)
    ]

    def shoot(self):
        self.__weapon__.shoot(Damage(self, TechData.get_normal_attack() + 1))

    def delta(self) -> vec2:
        self.idx = 2
        if self.__state__ == MoveState.idle:
            if self.phase == 1 or self.phase == 2:
                return vec2(4, 8)
            else:
                return vec2(6, 8)

        elif self.__state__ == MoveState.run:
            return self.__runPos__[self.phase]

        elif self.__state__ == MoveState.jump:
            return self.__jumpPos__[self.phase] - vec2((2 if self.idx >= 1 else -2), 4 - self.idx * 2)

    def update(self, args: GameArgs):
        self.__state__ = self.__follow__.__state__
        flip = self.__follow__.image.flip
        self.image.flip = flip
        self.phase = self.__follow__.image.indexX
        d = self.delta()
        wd = self.__weaponMove__[self.idx - 1] * 2
        if flip:
            d = vec2(-d.x, d.y)
            wd = vec2(-wd.x, wd.y)
        self.__weapon__.image.flip = flip

        self.centre = self.__follow__.centre + d
        self.__weapon__.centre = self.centre + wd
        pass

    def draw(self, render_args: RenderArgs):
        if not isinstance(self.image, MultiImage):
            raise Exception()
        self.__weapon__.draw(render_args)
        self.image.set_image(self.idx - 1)
        self.image.draw_self(render_args, self.centre)


class Player(MovableEntity):
    __state__: MoveState = MoveState.idle
    __image_set__: MultiImageSet
    __hand__: PlayerHand
    ammunition: int
    fire_cooldown: float

    def __init__(self, position: vec2 = vec2(24, 0), speed: vec2 = vec2(0, 0)):
        super().__init__()
        self.ammunition = 10
        self.fire_cooldown = 1
        s = MultiImageSet(vec2(32, 48), vec2(48, 48), 'Characters\\Player')
        self.__hand__ = PlayerHand(self)
        self.__image_set__ = s
        self.image = s
        self.hp = HPBar(self)
        self.fractionLock = False
        self.gravity = 9.8
        self.size = vec2(40, 96 - 24)
        self.boundAnchor = vec2(20, 48 - 24)
        self.centre = position
        self.__ySpeed__ = speed.y
        self.__lastSpeedX__ = speed.x
        s.scale = 2.0
        s.imageSource = s.imageDict['Punk_run']
        self.physicSurfName = 'player'

    def draw(self, render_args: RenderArgs):
        self.__hand__.draw(render_args)
        self.image.draw_self(render_args, centre=self.centre)

    __x_moving__: bool = False
    __step_timing__: float = 0.0

    hp: HPBar
    jump_speed = 9.8

    @property
    def state(self) -> MoveState:
        return self.__state__

    @state.setter
    def state(self, val: MoveState):
        if val == self.__state__:
            return
        self.__state__ = val
        self.__step_timing__ = 0
        self.image.indexX = 0

    __jumpPressTime__ = 0.0
    __walkEffectTime__ = 0.0

    def attack(self):
        self.__hand__.shoot()
        Sounds.shoot.set_volume(0.19)
        Sounds.shoot.play()

    def dispose(self):
        super().dispose()

    def died(self):
        instance_create(DelayedAction(0, Action(self.dispose)))
        GameState.__gsScene__.remove_player()
        Sounds.died.play()
        return

    def deal_damage(self, damage: Damage):
        self.hp.take_damage(damage.damageLevel)
        self.jump(4 + 2 * damage.damageLevel)

        if damage.source.centre.x > self.centre.x:
            self.give_force(-13)
        else:
            self.give_force(13)

        Sounds.player_damaged.play()

    def update(self, args: GameArgs):
        speed_x_target = 0
        if key_hold(pygame.K_LEFT) or key_hold(pygame.K_a):
            speed_x_target -= 5
        if key_hold(pygame.K_RIGHT) or key_hold(pygame.K_d):
            speed_x_target += 5

        self.__moveIntention__.x = speed_x_target
        if speed_x_target > 0:
            self.image.flip = False
        if speed_x_target < 0:
            self.image.flip = True

        if self.fire_cooldown <= 0:
            if key_on_press(pygame.K_SPACE) or key_on_press(pygame.K_j):
                self.attack()
                self.ammunition -= 1
            if self.ammunition == 0:
                self.fire_cooldown = 1
                self.ammunition = 10

        if self.fire_cooldown > 0:
            self.fire_cooldown -= args.elapsedSec

        need_jump = key_hold(pygame.K_c) or key_hold(pygame.K_w)
        if need_jump:
            self.__jumpPressTime__ += args.elapsedSec
        else:
            self.__jumpPressTime__ = 0

        if need_jump and self.onGround and self.__jumpPressTime__ < 0.1:
            self.jump(self.jump_speed)
            self.state = MoveState.jump

            instance_create(MoveSmoke(
                vec2(self.centre.x, self.areaRect.bottom - 36),
                0,
                'Characters\\Player\\Effect\\Jump\\0.png',
                4
            ))

        if self.__ySpeed__ < 0 and not need_jump:
            self.gravity = 43
        else:
            self.gravity = 9.8

        d = self.move(args)

        if abs(d.x) > 1e-8:
            if self.onGround:
                self.state = MoveState.run

        else:
            if self.onGround:
                self.state = MoveState.idle

        self.__step_timing__ += args.elapsedSec

        if self.state == MoveState.run:
            self.image.imageSource = self.__image_set__.imageDict['Punk_run']

            if self.onGround:
                self.__walkEffectTime__ += args.elapsedSec

            if self.__walkEffectTime__ >= 0.16:
                self.__walkEffectTime__ -= 0.16
                instance_create(MoveSmoke(
                    vec2(self.centre.x, self.areaRect.bottom - 36),
                    self.__lastSpeedX__,
                    'Characters\\Player\\Effect\\Walk\\' + str(Math.rand(0, 2)) + '.png')
                )

            if self.__step_timing__ > 0.1:
                self.__step_timing__ -= 0.1
                if abs(d.x) > 0:
                    self.image.indexX += 1
                    if self.image.indexX >= 6:
                        self.image.indexX = 0

        elif self.state == MoveState.idle:
            self.image.imageSource = self.__image_set__.imageDict['Punk_idle']
            if self.__step_timing__ > 0.2:
                self.__step_timing__ -= 0.2
                self.image.indexX += 1
                if self.image.indexX >= 4:
                    self.image.indexX = 0

        elif self.state == MoveState.jump:
            self.image.imageSource = self.__image_set__.imageDict['Punk_jump']
            if self.__ySpeed__ < -self.jump_speed * 0.5:
                self.image.indexX = 0
            elif self.__ySpeed__ < 0:
                self.image.indexX = 1
            elif self.__ySpeed__ < self.jump_speed * 0.35:
                self.image.indexX = 2
            else:
                self.image.indexX = 3

        self.__hand__.update(args)

