from pygame import *
from pygame.mixer import Sound


def load_image(path: str) -> Surface:
    return image.load('Resources\\Images\\' + path).convert_alpha()


def load_sound(path: str) -> Sound:
    return Sound('Resources\\Audio\\Sounds\\' + path)

