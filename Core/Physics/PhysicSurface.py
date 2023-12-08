from Core.GameStates.ObjectManager import *
from Core.Physics.Collidable import *
from typing import *


class PhysicObjectManager:
    __collidables__: set

    def __init__(self):
        self.__collidables__ = set()

    def instance_create(self, obj: GameObject):
        self.__collidables__.add(obj)

    def get_objects(self) -> Set[Collidable]:
        return self.__collidables__

    def collect(self):
        for obj in list(self.__collidables__):
            if obj.is_disposed():
                self.__collidables__.remove(obj)


class PhysicSurface:
    name: str
    __objects__: PhysicObjectManager

    def __init__(self, s: str):
        self.name = s
        self.__objects__ = PhysicObjectManager()

    def add_object(self, obj: (GameObject, Collidable)):
        self.__objects__.instance_create(obj)

    def frame_reset(self):
        self.__objects__.collect()

    def get_objects(self) -> Set[Collidable]:
        return self.__objects__.get_objects()

    def check_with(self, another):
        objs1 = self.get_objects()
        objs2 = another.get_objects()
        if len(objs1) * len(objs2) > 10000:
            # too much objects. need optimize
            raise NotImplementedError()

        for obj in objs1:
            for tar in objs2:
                if obj.physicArea.CollideWith(tar.physicArea):
                    obj.on_collide(tar)
                    tar.on_collide(obj)
