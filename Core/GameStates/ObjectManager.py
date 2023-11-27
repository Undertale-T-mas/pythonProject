from typing import *
from Core.GameObject import *


class ObjectManager:

    __objects__: List[GameObject] = []

    __buffer__: List[GameObject] = []

    __idx__: Set[int] = set()
    __idx_list__: List[int] = []

    __idx_cnt__ = 0

    def instance_create(self, obj: GameObject):
        self.__buffer__.append(obj)

    def get_objects(self):
        objects : List[GameObject] = []
        for obj in self.__objects__:
            if not obj.is_disposed():
                objects.append(obj)
        return objects

    def push_buffer(self):
        for obj in self.__buffer__:
            if self.__idx_cnt__ > 0:
                tar = self.__idx_list__[-1]
                self.__idx_list__.pop()
                self.__idx__.remove(tar)
                self.__idx_cnt__ -= 1
                self.__objects__[tar] = obj
            else:
                self.__objects__.append(obj)
        self.__buffer__.clear()

    def collect(self):
        i = 0
        for obj in self.__objects__:
            if obj.is_disposed():
                self.__idx__.add(i)
                self.__idx_list__.append(i)
                self.__idx_cnt__ += 1
            i += 1

    def update_all(self, args: GameArgs):
        self.push_buffer()

        i = 0
        for obj in self.__objects__:
            if not obj.is_disposed():
                obj.update(args)
            else:
                if i not in self.__idx__:
                    self.__idx__.add(i)
                    self.__idx_list__.append(i)
                    self.__idx_cnt__ += 1
            i += 1
