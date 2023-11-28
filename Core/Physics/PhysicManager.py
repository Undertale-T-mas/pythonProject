from typing import *
from Core.Physics.PhysicSurface import *


class PhysicManager:
    __surfMap__: Dict[str, PhysicSurface] = dict()
    __surfs__: Set[PhysicSurface] = set()

    def insert_object(self, obj: GameObject):
        if not isinstance(obj, Collidable):
            raise Exception()
        s = obj.physicSurfName
        if s not in self.__surfMap__:
            sur = PhysicSurface()
            self.__surfs__.add(sur)
            self.__surfMap__[s] = sur
        self.__surfMap__[s].add_object(obj)

    def frame_reset(self):
        for sur in self.__surfs__:
            sur.frame_reset()

    def update(self):
        raise NotImplementedError()
