from Core.GameObject import *
from Core.GameStates.GameStates import *
import pygame

from Core.Physics.Collidable import *
from Game.Characters.Movable import *


class MoveState(Enum):
    idle = 0,
    run = 1,
    jump = 2


class Player(MovableEntity):

    __state__: MoveState = MoveState.idle
    __image_set__: MultiImageSet

    def __init__(self):
        self.physicSurfName = 'player'
        super().__init__()
        s = MultiImageSet(vec2(32, 48), vec2(48, 48), 'Characters\\Player')
        self.__image_set__ = s
        self.image = s
        self.gravity = 9.8
        self.size = vec2(40, 96 - 24)
        self.boundAnchor = vec2(20, 48 - 24)
        self.centre = vec2(24, 0)
        s.scale = 2.0
        s.imageSource = s.imageDict['Punk_run']

    def draw(self, render_args: RenderArgs):
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

    def update(self, args: GameArgs):
        if key_hold(pygame.K_LEFT):
            self.__moveIntention__.x = -5
            self.image.flip = True
        if key_hold(pygame.K_RIGHT):
            self.__moveIntention__.x = 5
            self.image.flip = False

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

