from Core.GameObject import IUpdatable
from Core.Physics.CollidingArea import CollideArea


class Collidable(IUpdatable):
    physicSurfName: str
    physicArea: CollideArea

    def on_collide(self, another):
        raise NotImplementedError()
