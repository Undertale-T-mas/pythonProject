from Core.GameObject import *
from Core.GameStates.GameStates import *
import pygame

from Core.Physics.Collidable import *


class Player(Entity, Collidable):
    def __init__(self):
        super().__init__()
        self.image = MultiImageSet(vec2(32, 48), vec2(48, 48), 'Characters\\Player')
        self.image.scale = 2.0

    def draw(self, render_args: RenderArgs):
        self.image.draw_self(render_args, centre=self.centre)

    def update(self, args: GameArgs):
        if key_hold(pygame.K_w):
            self.centre.y -= 5
        if key_hold(pygame.K_s):
            self.centre.y += 5
        if key_hold(pygame.K_a):
            self.centre.x -= 5
        if key_hold(pygame.K_d):
            self.centre.x += 5

