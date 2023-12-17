from pygame.font import Font
from pygame.mixer import Sound
from pygame import font
from Resources.ResourceLoad import *

__font_sizes__: Dict[Font, int] = dict()


class Fonts:
    done_direct: Font = None
    evil_empire: Font = None
    kwark: Font = None
    glitch_goblin: Font = None

    @staticmethod
    def init_font(path, size) -> Font:
        res = load_font(path, size)
        __font_sizes__[res] = size
        return res

    @staticmethod
    def initialize():
        Fonts.done_direct = Fonts.init_font('DoneDirect.otf', 40)
        Fonts.glitch_goblin = Fonts.init_font('GlitchGoblin.ttf', 20)
        Fonts.evil_empire = Fonts.init_font('EvilEmpire.ttf', 72)
        Fonts.kwark = Fonts.init_font('Kwark.ttf', 72)

    @staticmethod
    def seek_size(f: Font) -> int:
        return __font_sizes__[f]


class Sounds:
    startGame: Sound = None
    shoot: Sound = None
    laser: Sound = None
    died: Sound = None
    jump: Sound = None
    playerDamaged: Sound = None
    robotDamaged: Sound = None
    recharge: Sound = None
    robotDied: Sound = None
    jumpLand: Sound = None

    @staticmethod
    def initialize():
        Sounds.recharge = load_sound('recharge.wav')
        Sounds.startGame = load_sound('start.wav')
        Sounds.shoot = load_sound('shoot.wav')
        Sounds.laser = load_sound('laser.wav')
        Sounds.died = load_sound('died.wav')
        Sounds.jump = load_sound('jump.wav')
        Sounds.jumpLand = load_sound('jumpland.wav')
        Sounds.playerDamaged = load_sound('player_damaged.wav')
        Sounds.robotDamaged = load_sound('robot_damaged.wav')
        Sounds.robotDied = load_sound('robot_died.wav')
