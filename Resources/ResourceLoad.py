from pygame import *


def load_image(path: str) -> Surface:
    return image.load('Resources\\Images\\' + path).convert_alpha()
