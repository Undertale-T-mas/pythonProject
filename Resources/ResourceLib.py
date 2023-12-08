from pygame.mixer import Sound

from Resources.ResourceLoad import *


class Sounds:
    startGame: Sound = None
    shoot: Sound = None
    laser: Sound = None
    died: Sound = None
    player_damaged: Sound = None
    robot_damaged: Sound = None

    @staticmethod
    def initialize():
        Sounds.startGame = load_sound('start.wav')
        Sounds.shoot = load_sound('shoot.wav')
        Sounds.laser = load_sound('laser.wav')
        Sounds.died = load_sound('died.wav')
        Sounds.player_damaged = load_sound('player_damaged.wav')
        Sounds.robot_damaged = load_sound('robot_damaged.wav')