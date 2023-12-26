from Core.Profile.Savable import *
from Game.Barrage.Barrage import Barrage
from Game.Characters.Movable import Damage
from Game.Map.Framework.Tiles import *
from core import *
from Game.Map.Objects.ObjectBase import MapObjectFuncBase


class CannonBullet(Barrage):
    rect: CollideRect

    def __init__(self, path: str, start: vec2, flip: bool, speed: vec2, direction: float, damage: Damage):
        super().__init__(damage)
        if damage.source is None:
            damage.source = self
        self.image = SingleImage(path)
        self.move(EasingGenerator.linear(start, speed))
        self.image.scale = 1.5
        self.image.rotation = direction
        self.image.flip = flip
        self.autoDispose = True
        self.physicSurfName = 'barrage'
        self.rect = CollideRect()
        self.rect.area = FRect(0, 0, 1, 1)
        self.physicArea = self.rect

    def update(self, args: GameArgs):
        self.rect.area.centre = self.centre
        super().update(args)

    def draw(self, render_args: RenderArgs):
        self.image.draw_self(render_args, self.centre)

    def on_collide(self, another):
        super().on_collide(another)


class Cannon(MapObjectFuncBase):
    direction: float
    interval: any

    t: float

    def shoot(self, pos: vec2):
        instance_create(
            CannonBullet(
                'Objects\\Barrage\\Cannon_bullet.png',
                pos + Math.vec2_polar(56, self.direction),
                False,
                Math.vec2_polar(900, self.direction),
                self.direction,
                Damage(damage_level=1)
            )
        )
        pass

    def on_create(self, pos_x: int, pos_y: int):
        pass

    def on_update(self, object_source: Entity):
        self.t -= self.args.elapsedSec
        object_source.image.rotation = self.direction
        if self.t <= 0:
            self.t += self.interval
            self.shoot(object_source.centre)
        pass

    def __init__(self, direction: float, interval: float):
        self.direction = direction
        self.t = interval
        self.interval = interval
        super().__init__()



