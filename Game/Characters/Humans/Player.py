from Core.GameObject import *
from Core.GameStates.GameStates import *
import pygame

from Core.Physics.Collidable import *
from Game.Characters.Movable import *


class MoveState(Enum):
    idle = 0,
    run = 1,
    jump = 2,


class PlayerHand(Entity):
    def __init__(self, follow):
        self.__follow__ = follow
        self.image = MultiImage('Characters\\Player\\Hands')
        self.image.scale = 2

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
        vec2(7, 7)
    ]
    __jumpPos__: List[vec2] = [
        vec2(12, 6),
        vec2(12, 4),
        vec2(12, 2),
        vec2(12, 5)
    ]

    def delta(self) -> vec2:
        if not self.__inAttack__:
            if self.idx == 3:
                self.idx = 1
        if self.__state__ == MoveState.idle:
            if self.phase == 1 or self.phase == 2:
                return vec2(4, 8)
            else:
                return vec2(6, 8)

        elif self.__state__ == MoveState.run:
            return self.__runPos__[self.phase]

        elif self.__state__ == MoveState.jump:
            if self.idx == 1:
                self.idx = 3
            return self.__jumpPos__[self.phase] - vec2(3, 0)

    def update(self, args: GameArgs):
        self.__state__ = self.__follow__.__state__
        self.phase = self.__follow__.image.indexX
        self.centre = self.__follow__.centre + self.delta()
        pass

    def draw(self, render_args: RenderArgs):
        if not isinstance(self.image, MultiImage):
            raise Exception()
        self.image.set_image(self.idx - 1)
        self.image.draw_self(render_args, self.centre)


class Player(MovableEntity):

    __state__: MoveState = MoveState.idle
    __image_set__: MultiImageSet
    __hand__: PlayerHand

    def __init__(self):
        self.physicSurfName = 'player'
        super().__init__()
        s = MultiImageSet(vec2(32, 48), vec2(48, 48), 'Characters\\Player')
        self.__hand__ = PlayerHand(self)
        self.__image_set__ = s
        self.image = s
        self.gravity = 9.8
        self.size = vec2(40, 96 - 24)
        self.boundAnchor = vec2(20, 48 - 24)
        self.centre = vec2(24, 0)
        s.scale = 2.0
        s.imageSource = s.imageDict['Punk_run']

    def draw(self, render_args: RenderArgs):
        self.__hand__.draw(render_args)
        self.image.draw_self(render_args, centre=self.centre)

    __x_moving__: bool = False
    __step_timing__: float = 0.0

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

    def attack(self):
        pass

    def update(self, args: GameArgs):
        if key_hold(pygame.K_LEFT):
            self.__moveIntention__.x = -5
            self.image.flip = True
        if key_hold(pygame.K_RIGHT):
            self.__moveIntention__.x = 5
            self.image.flip = False

        if key_on_press(pygame.K_SPACE):
            self.attack()

        need_jump = key_hold(pygame.K_c)
        if need_jump:
            self.__jumpPressTime__ += args.elapsedSec
        else:
            self.__jumpPressTime__ = 0

        if need_jump and self.onGround and self.__jumpPressTime__ < 0.1:
            self.jump(self.jump_speed)
            self.state = MoveState.jump

        if self.__ySpeed__ < 0 and not need_jump:
            self.gravity = 33
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
            if d.y < -self.jump_speed * 0.5:
                self.image.indexX = 0
            elif d.y < 0:
                self.image.indexX = 1
            elif d.y < self.jump_speed * 0.5:
                self.image.indexX = 2
            else:
                self.image.indexX = 3

        self.__hand__.update(args)

