from pygame.mixer import Sound

from Resources.ResourceLoad import *


class Sounds:
    startGame: Sound = load_sound('start.wav')
    attack: Sound = load_sound('attack.wav')
    laser: Sound = load_sound('laser.wav')
    died: Sound = load_sound('died.wav')
