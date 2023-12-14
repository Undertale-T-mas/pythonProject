from pygame.font import Font
from pygame.mixer import Sound
from pygame import font
from Resources.ResourceLoad import *


class Fonts:
    done_direct: Font = None
    evil_empire: Font = None
    kwark: Font = None

    @staticmethod
    def initialize():
        Fonts.done_direct = load_font('DoneDirect.otf', 24)
        Fonts.evil_empire = load_font('EvilEmpire.ttf', 72)
        Fonts.kwark = load_font('Kwark.ttf', 72)


class Sounds:
    startGame: Sound = None
    shoot: Sound = None
    laser: Sound = None
    died: Sound = None
    player_damaged: Sound = None
    robot_damaged: Sound = None
    recharge: Sound = None
    robot_died: Sound = None

    @staticmethod
    def initialize():
        Sounds.recharge = load_sound('recharge.wav')
        Sounds.startGame = load_sound('start.wav')
        Sounds.shoot = load_sound('shoot.wav')
        Sounds.laser = load_sound('laser.wav')
        Sounds.died = load_sound('died.wav')
        Sounds.player_damaged = load_sound('player_damaged.wav')
        Sounds.robot_damaged = load_sound('robot_damaged.wav')
        Sounds.robot_died = load_sound('robot_died.wav')
