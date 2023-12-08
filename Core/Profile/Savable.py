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
        return self.__val__

    @value.setter
    def value(self, val: T):
        self.__val__ = val
        ProfileIO.set(self.path_with_obj, val)
