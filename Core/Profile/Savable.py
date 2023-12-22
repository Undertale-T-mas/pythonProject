import builtins
from enum import Enum
from math import *

import Core.GameStates.GameState
from Core.GameObject import *
from Core.Profile.ProfileIO import *

T = TypeVar("T")


class Savable(Generic[T]):
    path_with_obj: str
    __val__: Any = None

    def __init__(self, path_with_obj):
        self.path_with_obj = path_with_obj
        self.__val__ = ProfileIO.get(self.path_with_obj)

    @property
    def value(self) -> T:
        if self.__val__ is None:
            self.__val__ = ProfileIO.get(self.path_with_obj)
        return self.__val__

    @value.setter
    def value(self, val: T):
        self.__val__ = val
        ProfileIO.set(self.path_with_obj, val)

    def __int__(self):
        return int(self.__val__)

    def __str__(self):
        return str(self.__val__)

    def __float__(self):
        return float(self.__val__)

    def __add__(self, other):
        return self.__val__ + other

    def __sub__(self, other):
        return self.__val__ - other

    def __mul__(self, other):
        return self.__val__ * other

    def __eq__(self, other):
        return self.__val__ == other

    def __divmod__(self, other):
        return divmod(self.__val__, other)

