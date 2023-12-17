from Game.Characters.Movable import Damage
from core import *


class Barrage(Entity, Collidable):
    autoDispose: bool
    pierce: bool
    damage: Damage

    def __init__(self, damage: Damage):
        super().__init__()
        self.autoDispose = True
        self.pierce = False
        self.damage = damage

    def __set_centre__(self, result: vec2):
        self.centre = result
        self.physicSurfName = 'barrage'
        self.surfaceName = 'barrage'

    def move(self, ease: EasingRunner | Easing):
        if isinstance(ease, Easing):
            ease = EasingRunner(ease.time, ease.start, ease.end, ease)
        ease.run(self.__set_centre__, self)

    def update(self, args: GameArgs):
        if self.centre.x < -200 or self.centre.x > GameState.__gsRenderOptions__.screenSize.x + 200:
            self.dispose()
        if self.centre.y < -200 or self.centre.y > GameState.__gsRenderOptions__.screenSize.y + 200:
            self.dispose()

    def on_collide(self, another):
        if not self.pierce:
            self.dispose()
