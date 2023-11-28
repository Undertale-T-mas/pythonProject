from Core.Physics.CollidingArea import CollideArea


class Collidable:
    physicSurfName: str
    physicArea: CollideArea

    def on_collide(self, another):
        raise NotImplementedError()
