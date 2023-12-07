from typing import *
from Core.Physics.PhysicSurface import *


class PhysicManager:
    __surfMap__: Dict[str, PhysicSurface]
    __surfs__: Set[PhysicSurface]

    def __init__(self):
        self.__surfs__ = set()
        self.__surfMap__ = dict()

    def insert_object(self, obj: GameObject):
        if not isinstance(obj, Collidable):
            raise Exception()
        s = obj.physicSurfName
        if s not in self.__surfMap__:
            sur = PhysicSurface(s)
            self.__surfs__.add(sur)
            self.__surfMap__[s] = sur
        self.__surfMap__[s].add_object(obj)

    def frame_reset(self):
        for sur in self.__surfs__:
            sur.frame_reset()

    def update(self):
        self.frame_reset()

    def check(self, source: str, destin: str):
        if source not in self.__surfMap__.keys() or destin not in self.__surfMap__.keys():
            return
        source = self.__surfMap__[source]
        destin = self.__surfMap__[destin]
        source.check_with(destin)
