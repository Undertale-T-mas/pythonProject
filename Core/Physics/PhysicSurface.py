from Core.GameStates.ObjectManager import *
from Core.Physics.Collidable import *
from typing import *


class PhysicSurface:
    name: str
    __objects__: ObjectManager

    def __init__(self, s: str):
        self.name = s
        self.__objects__ = ObjectManager()

    def add_object(self, obj: (GameObject, Collidable)):
        self.__objects__.instance_create(obj)

    def frame_reset(self):
        self.__objects__.collect()
        self.__objects__.push_buffer()

    def get_objects(self) -> List[Collidable]:
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
