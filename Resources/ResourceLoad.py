from pygame import *
from pygame.mixer import Sound
from typing import *


__imgLoadBuffer__: Dict[str, Surface] = dict()


def load_image(path: str) -> Surface:
    if path in __imgLoadBuffer__:
        return __imgLoadBuffer__[path]
    res = image.load('Resources\\Images\\' + path).convert_alpha()
    __imgLoadBuffer__[path] = res
    return res


def load_sound(path: str) -> Sound:
    return Sound('Resources\\Audio\\Sounds\\' + path)

