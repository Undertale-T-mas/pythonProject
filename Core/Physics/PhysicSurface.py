from Core.GameStates.ObjectManager import *
from Core.Physics.Collidable import *
from typing import *


class PhysicSurface:
    name: str
    __objects__: ObjectManager

    def add_object(self, obj: (GameObject, Collidable)):
        self.__objects__.instance_create(obj)

    def frame_reset(self):
        self.__objects__.collect()
        self.__objects__.push_buffer()

    def get_objects(self) -> List[Collidable]:
        return self.__objects__.get_objects()

