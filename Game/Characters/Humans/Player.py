from Game.Barrage.Barrage import *
from Game.Characters.Humans.Data import PlayerData, IPlayer
from Game.Characters.Humans.HPBar import HPBar
from Game.Characters.Humans.Save import SavingSlot
from Game.Characters.Movable import *
from Game.Tech.DataLib import TechData
from Resources.ResourceLib import *

from core import *


class MoveState(Enum):
    idle = 0,
    run = 1,
    jump = 2,


class PlayerBullet(Barrage):
    rect: CollideRect
    tiles: TileMap

    def __init__(self, start: vec2, d: bool, damage: Damage, tiles: TileMap):
        super().__init__(damage)
        self.image = MultiImage('Characters\\Player\\Bullets')
        self.physicSurfName = 'pl_bullet'
        self.move(EasingGenerator.linear(start, vec2(-1100, 0) if d else vec2(1100, 0)))
        self.image.scale = 2
        self.tiles = tiles
        self.centre = start
        self.image.flip = d
        self.autoDispose = True
        self.rect = CollideRect()
        self.rect.area = FRect(0, 0, 1, 3)
        self.physicArea = self.rect

    def update(self, args: GameArgs):
        self.rect.area.centre = self.centre
        super().update(args)
        decx = int(self.centre.x // TILE_LENGTH)
        decy = int(self.centre.y // TILE_LENGTH)
        if self.tiles is None:
            return
        for i in range(3):
            tar = self.tiles.get_tile(decx, decy + i - 1)
            if tar.uuid == 0:
                continue
            if tar.collidable:
                if not isinstance(self.physicArea, CollideRect):
                    raise Exception()
                if self.physicArea.area.collide_rect(tar.areaRect):
                    self.dispose()

                    img = ImageSet(
                        vec2(48, 48),
                        vec2(48, 48),
                        'Effects\\Sparks\\' + str(Math.rand(0, 2)) + '.png'
                    )
                    if self.image.flip:
                        img.flip = True
                    img.scale = 1.5
                    instance_create(Animation(
                        img,
                        0.05,
                        self.centre - vec2(0, 10)
                    ))

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
    tiles: TileMap

    def __init__(self):
        super().__init__()
        self.image = MultiImage('Characters\\Player\\Weapons')
        self.image.scale = 2
        self.tiles = None

    def update(self, args: GameArgs):
        if self.tiles is None:
            self.tiles = GameState.__gsScene__.__tileMap__
        self.idx = 0
        self.image.imageSource = self.image.imageList[0]

    def draw(self, render_args: RenderArgs):
        self.image.draw_self(render_args, self.centre)

    def shoot(self, damage: Damage):
        d = self.delta[self.idx]
        if self.image.flip:
            d = vec2(-d.x, d.y)
        instance_create(PlayerBullet(self.centre + d, self.image.flip, damage, self.tiles))
        ani_img = ImageSet(vec2(48, 48), vec2(48, 48), 'Effects\\Gun\\0.png')
        ani_img.flip = self.image.flip
        ani_img.scale = 2.0
        ani_img.alpha = 0.7
        anim = Animation(
            ani_img,
            0.03,
            self.centre + vec2(-68 if self.image.flip else 68, -2)
        )
        instance_create(anim)

        def follow():
            anim.image.flip = self.image.__flip__
            anim.centre = self.centre + vec2(-68 if self.image.flip else 68, -2)

        instance_create(StableAction(0.4, Action(follow)))

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
        super().__init__()
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
        self.__weapon__.update(args)

    def draw(self, render_args: RenderArgs):
        if not isinstance(self.image, MultiImage):
            raise Exception()
        self.__weapon__.draw(render_args)
        self.image.set_image(self.idx - 1)
        self.image.draw_self(render_args, self.centre)


class Player(MovableEntity, IPlayer):
    __state__: MoveState = MoveState.idle
    __image_set__: MultiImageSet
    __hand__: PlayerHand
    __saver__: SavingSlot

    ammunition: int
    fire_cooldown: float

    def __init__(self, position: vec2 = vec2(24, 0), speed: vec2 = vec2(0, 0), data: PlayerData = PlayerData()):
        super().__init__()
        self.__saver__ = SavingSlot()
        self.ammunition = data.ammunition
        self.fire_cooldown = data.fire_cooldown
        s = MultiImageSet(vec2(32, 48), vec2(48, 48), 'Characters\\Player')
        self.__hand__ = PlayerHand(self)
        self.__image_set__ = s
        self.image = s
        self.hp = HPBar(self)
        self.hp.__hp__ = min(data.hp, self.hp.hp_max)
        self.fractionLock = False
        self.gravity = 9.8
        self.size = vec2(40, 96 - 21)
        self.boundAnchor = vec2(20, 48 - 21)
        self.centre = position
        self.__ySpeed__ = speed.y
        self.__lastSpeedX__ = speed.x
        self.__jumpPressTime__ = 0.0
        self.__dead__ = False
        s.scale = 2.0
        s.imageSource = s.imageDict['Punk_run']
        self.physicSurfName = 'player'
        self.__leaveGroundTime__ = 1.0
        self.__walkEffectTime__ = 0.0
        self.__step_timing__ = 0.0
        self.jump_speed = 9.8
        self.__x_moving__ = False

    def on_collide(self, another):
        if not isinstance(another, Barrage):
            raise Exception()
        self.deal_damage(another.damage)

    def draw(self, render_args: RenderArgs):
        self.__hand__.draw(render_args)
        self.image.draw_self(render_args, centre=self.centre)

    @property
    def data(self) -> PlayerData:
        return PlayerData(self.ammunition, self.fire_cooldown, self.hp.__hp__, obj=self)

    __x_moving__: bool
    __step_timing__: float

    hp: HPBar
    jump_speed: float

    @property
    def state(self) -> MoveState:
        return self.__state__

    @state.setter
    def state(self, val: MoveState):
        if val == self.__state__:
            return
        self.__state__ = val
        self.__step_timing__ = 0.0
        self.image.indexX = 0

    __jumpPressTime__: float
    __walkEffectTime__: float
    __leaveGroundTime__: float

    def attack(self):
        self.__hand__.shoot()
        Sounds.shoot.set_volume(0.19)
        Sounds.shoot.play()

    def dispose(self):
        super().dispose()

    __dead__: bool

    def died(self):
        instance_create(DelayedAction(0, Action(self.dispose)))
        shake_dir = 0.0
        if self.__inVoid__:
            shake_dir = 90.0
            Sounds.jumpLand.set_volume(1)
            Sounds.jumpLand.play()
            for i in range(3):
                img_set = ImageSet(vec2(48, 48), vec2(48, 48), 'Effects\\Void\\0.png')
                img_set.scale = 2.5 + i * 0.3
                img_set.alpha = 1.0 - i * 0.3
                instance_create(
                    Animation(
                        img_set,
                        0.06 + i * 0.015, vec2(self.centre.x, GameState.__gsRenderOptions__.screenSize.y - 58 - 72 + i * 21),
                        True, 'barrage'
                    )
                )
        else:
            shake_dir = Math.rand(0, 359)
            img_set = ImageSet(vec2(48, 48), vec2(48, 48), 'Effects\\Blood\\0.png')
            img_set.scale = 2.0
            instance_create(
                Animation(
                    img_set,
                    0.08, self.centre + vec2(8, 16), True, 'barrage'
                )
            )
        GameState.__gsScene__.remove_player(shake_dir, self.centre)
        Sounds.died.play()
        self.__dead__ = True
        return

    def deal_damage(self, damage: Damage):
        self.hp.take_damage(damage.damageLevel)
        self.jump(4 + 2 * damage.damageLevel)

        if damage.source.centre.x > self.centre.x:
            self.give_force(-13)
        else:
            self.give_force(13)

        Sounds.playerDamaged.play()

    def recharge_time(self):
        return 0.7

    def recharge(self):
        self.fire_cooldown = self.recharge_time()
        self.ammunition = 7

        instance_create(DelayedAction(0.15, Action(Sounds.recharge.play)))

    def on_land(self):
        Sounds.jumpLand.set_volume(min(1.0, pow(self.__ySpeed__ * 0.0375, 2.5)))
        Sounds.jumpLand.play()

        instance_create(MoveSmoke(
            vec2(self.centre.x, self.areaRect.bottom - 36),
            0,
            'Characters\\Player\\Effect\\Jump\\0.png',
            4
        ))

    def hp_max(self):
        return self.hp.hp_max

    def save_slot_acceptable(self):
        return self.__saver__.acceptable()

    def gather_save(self):
        self.__saver__.push()

    def save_progress(self):
        return self.__saver__.progress()

    def save_slot_energy(self):
        return self.__saver__.count.value

    def save_slot_size(self):
        return self.__saver__.slot_size()

    def update(self, args: GameArgs):
        speed_x_target = 0
        if key_hold(ki.left):
            speed_x_target -= 5
        if key_hold(ki.right):
            speed_x_target += 5

        self.__moveIntention__.x = speed_x_target
        if speed_x_target > 0:
            self.image.flip = False
        if speed_x_target < 0:
            self.image.flip = True

        if key_on_press(ki.recharge) and self.fire_cooldown <= 0:
            self.recharge()

        if self.fire_cooldown <= 0:
            if key_on_press(ki.shoot):
                self.attack()
                self.ammunition -= 1
            if self.ammunition == 0:
                self.recharge()

        if self.fire_cooldown > 0:
            self.fire_cooldown -= args.elapsedSec

        need_jump = key_hold(ki.jump)
        if need_jump:
            self.__jumpPressTime__ += args.elapsedSec
        else:
            self.__jumpPressTime__ = 0

        if self.onGround:
            self.__leaveGroundTime__ = 0
        else:
            self.__leaveGroundTime__ += args.elapsedSec

        if need_jump and self.__leaveGroundTime__ < 0.062 and self.__jumpPressTime__ < 0.166:
            self.jump(self.jump_speed)
            self.__leaveGroundTime__ = 0.062
            Sounds.jump.set_volume(0.1)
            Sounds.jump.play()
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
        if self.__dead__:
            return

        if abs(d.x) > 1e-8:
            if self.onGround:
                self.state = MoveState.run

        else:
            if self.onGround:
                self.state = MoveState.idle

        self.__step_timing__ += args.elapsedSec

        if self.__ySpeed__ < -1:
            self.state = MoveState.jump

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
        self.data.update_data(self.ammunition, self.fire_cooldown, self.hp.__hp__, self.centre, self.hp.__difficulty__, self)
        self.__saver__.update(args)
