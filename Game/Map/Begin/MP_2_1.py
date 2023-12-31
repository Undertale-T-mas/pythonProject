import Resources.Music
from Game.Scenes.DemoEndScene import DemoEndScene
from core import *
from map import *
from Resources.Music import *


class BoolData:
    data: bool


class IRobot(LandRobot):

    def attack_a(self):
        raise NotImplementedError()

    def attack_b(self):
        raise NotImplementedError()

    def attack_r(self):
        raise NotImplementedError()

    def reset_state(self, s: str):
        raise NotImplementedError()


boss: IRobot | None = None
fight_ins: List[GameObject] = []


class Missile(Barrage):

    _mode: bool
    rect: CollideRect
    _speed: vec2

    _default_x: float

    def __init__(self, pos: vec2, speed_x: float, speed_y: float):
        super().__init__(Damage(self, 2))
        self.image = SingleImage('Objects\\Barrage\\Missile1.png')
        self.image.scale = 1.5

        self.centre = pos
        self._default_x = speed_x
        self._speed = vec2(speed_x, speed_y)
        self._mode = True
        rec = CollideRect()
        self.physicArea = rec
        self.rect = rec
        rec.area = FRect(0.0, 0.0, 2.0, 2.0)

    def update(self, args: GameArgs):

        pl = get_player_data()
        if self._mode:
            if self._speed.x > 0:
                if self.centre.x > pl.player_object.centre.x - 45:
                    self._mode = False
            else:
                if self.centre.x < pl.player_object.centre.x + 45:
                    self._mode = False

        self._speed = Math.lerp(
            self._speed,
            vec2(self._default_x, 0.0) if self._mode else vec2(0.0, 14.0),
            args.elapsedSec * 4.0
        )
        self._speed.x = Math.lerp(
            self._speed.x,
            self._default_x if self._mode else 0.0,
            args.elapsedSec * 12.0
        )

        self.centre += self._speed * args.elapsedSec * 60
        self.image.rotation = Math.dir_deg(self._speed)
        self.rect.area.centre = self.centre


class ToDemoEnd(GameObject):

    time_tot: float

    def __init__(self):
        super().__init__()
        self.time_tot = 0.0

    def update(self, args: GameArgs):
        self.time_tot += args.elapsedSec
        if self.time_tot >= 2:
            self.dispose()
            change_scene(DemoEndScene())
            return
        ro = GameState.__gsRenderOptions__.transform
        ro.alpha = 1 - self.time_tot * 0.5


class BossRobot0(IRobot):

    alp: float

    def __init__(self, *args):
        global boss
        boss = self

        self.__idxInterval__ = 0.1

        self.alp = 1.0

        if len(args) == 1:
            pos = args[0]
        else:
            pos = vec2((TILE_LENGTH + 0.5) * args[0], TILE_LENGTH * args[1] - 96.0 - 12.0)

        super().__init__(
            pos,
            MultiImageSet(vec2(96, 96), vec2(96, 96), 'Characters\\Enemys\\BOSS0'),
            vec2(48, 48 + 24.0), vec2(60, 192 + 24.0)
        )
        self.__hp__ = 2000.0
        self.__hp__ = 10.0
        self.__killed__ = False
        self._state = ''
        self.image.flip = True
        self.gravity = 0.0
        self.image.scale = 1.45 * 2.2
        self.killed_time = 0.0
        self.__state_cnt__ = {
            'Attack1': 4,
            'Attack3': 4,
            'Attack4': 4,
            'Death': 6,
            'Walk': 4,
            'Idle': 4,
        }
        self.move_speed = 0.0
        self.col = cv4.WHITE
        self.reset_state('Walk')

        ps = Surface(vec2(1, 1))
        ps.set_at((0, 0), Color(255, 255, 255, 255))
        self.pix = Texture(ps)

    def attack_a(self):
        if self.__killed__:
            return

        bul = RobotBullet(
            'Objects\\Barrage\\Laser1.png', self.centre + vec2(-80, 138.0),
            self.image.flip,
            vec2(-1300, 0),
            Damage(self, 1)
        )
        bul.image.scale = 5
        instance_create(bul)
        Sounds.laser.play()
        self.reset_state('Attack1')
        self.__idx__ = 1
        self.__idxInterval__ = 0.05

    def attack_b(self):
        if self.__killed__:
            return

        bul = RobotBullet(
            'Objects\\Barrage\\Laser1.png', self.centre + vec2(-20, -38.0),
            self.image.flip,
            vec2(-1300, 0),
            Damage(self, 1)
        )
        bul.image.scale = 4
        instance_create(bul)
        Sounds.laser.play()
        self.reset_state('Attack3')
        self.__idx__ = 1
        self.__idxInterval__ = 0.05

    def attack_r(self):
        if self.__killed__:
            return

        bul = Missile(self.centre + vec2(-30, -48.0), -12.0, -14.0)
        instance_create(bul)
        Sounds.laser.play()
        self.reset_state('Attack4')
        self.__idx__ = 1
        self.__idxInterval__ = 0.05

    col: vec4
    __idxInterval__: float
    pix: Texture

    def on_collide(self, another):
        if not isinstance(another, PlayerBullet):
            raise Exception()
        super().on_collide(another)
        self.deal_damage(another.damage.damageLevel)
        self.col = cv4.RED

    __killed__: bool
    __idx__: int
    _state: str
    _state_acc_time: float

    __state_cnt__: Dict[str, int]

    def on_state_finish(self):

        if self._state == 'Walk':
            self.reset_state('Walk')

        else:
            self.reset_state('Idle')

    def reset_state(self, state: str):
        if self._state == state:
            return
        if self._state == 'Death':
            return

        self.__idxInterval__ = 0.1

        self._state = state
        self.__idx__ = 0
        self._state_acc_time = 0

    def died(self):
        if self.__killed__:
            return
        Sounds.bomb.play()

        def died_anim_play():
            anim = Animation(
                ImageSet(vec2(64, 64), vec2(64, 64), 'Effects\\Explosion\\1.png'),
                0.03,
                self.centre + vec2(Math.rand(-100, 140), Math.rand(-40, 126)),
                scale=Math.rand_f(2.0, 2.8)
            )
            instance_create(anim)
            for obj in fight_ins:
                obj.dispose()
            stop_music()

        for i in range(20):
            instance_create(DelayedAction(0.1 * i, Action(died_anim_play)))

        self.__killed__ = True
        instance_create(DelayedAction(0.04, Action(Sounds.robotDied.play)))

    move_speed: float
    killed_time: float

    def update(self, args: GameArgs):
        super().update(args)

        self.col = Math.lerp(self.col, cv4.WHITE, min(1.0, args.elapsedSec * 20.0))

        if self.__killed__:
            self.killed_time += args.elapsedSec
            self.reset_state('Death')
            if self.killed_time >= 2.0:
                self.alp = 3.0 - self.killed_time
            if self.killed_time >= 3.0:
                instance_create(ToDemoEnd())
                self.dispose()
                return

        self.set_move_intention(vec2(self.move_speed, 0))
        self.move(args)
        self.image.indexX = self.__idx__

        if self._state_acc_time >= self.__idxInterval__:
            self.__idx__ += 1
            self._state_acc_time -= self.__idxInterval__
            pl = get_player_data()
            if pl.player_object.centre.x > self.areaRect.left - 40:
                pl.player_object.deal_damage(Damage(self, 0))
            if self.__idx__ >= self.__state_cnt__[self._state]:
                if self._state == 'Death':
                    self.__idx__ = self.__state_cnt__[self._state] - 1
                else:
                    self.__idx__ = 0
                    self.on_state_finish()
        self._state_acc_time += args.elapsedSec

        self.image.color = self.col
        self.__multiImage__.imageSource = self.__multiImage__.imageDict[self._state]
        self.image.alpha = self.alp

    def draw(self, render_args: RenderArgs):
        super().draw(render_args)

        render_args.target_surface.set_target_self()
        self.pix.draw(RenderData(self.centre - vec2(80, 100), anchor=None, scale=vec2(160, 20),
                                 color=vec4(0.75, 0.75, 0.75, 0.75)))
        self.pix.draw(RenderData(self.centre - vec2(80, 100), anchor=None, scale=vec2(160 * self.__hp__ / 2000.0, 20),
                                 color=vec4(0.75, 0.0, 0.0, 0.75)))


actions: Dict[str, Action] = dict()


def register_action(token: str, act: Action):
    actions[token] = act


def rhythm_activate(rhythm: List[str], interval: float, delta: float = 0.0):
    t = delta
    tl = TimeLine()
    fight_ins.append(tl)
    for i in range(len(rhythm)):
        s = rhythm[i]
        for unit in s.split(','):
            if unit == '':
                continue
            tl.insert(t, actions[unit])
        t += interval

    instance_create(tl)


map: TileMap


def introduce_attack_rhythm():

    def shoot_1():
        boss.attack_a()

    def shoot_2():
        boss.attack_b()

    def shoot_3():
        boss.attack_r()

    register_action('s', Action(shoot_1))
    register_action('t', Action(shoot_2))
    register_action('r', Action(shoot_3))

    rhythm_activate([
        '', '', '', '',        '', '', '', '',

        '', '', '', '',        's', '', '', '',
        's', '', '', '',        't', '', '', '',
        't', '', '', '',        's', '', 's', '',
        's', '', '', '',        't', '', 't', '',

        't', '', '', '',        's', '', 't', '',
        's', '', '', '',        't', '', 's', '',
        't', '', '', '',        's', '', 't', '',
        's', '', '', '',        't', '', 's', '',

        't', '', 'r', '',        't', '', 'r', '',
        't', '', 'r', '',        't', '', 'r', '',
        't', '', 'r', '',        't', '', 'r', '',
        't', '', 'r', '',        't', '', 'r', '',

        's', '', 'r', '',        's', '', 'r', '',
        's', '', 'r', '',        's', '', 'r', '',
        's', '', 'r', '',        's', '', 'r', '',
        's', '', 'r', '',        's', '', 'r', '',

        's,t', '', 'r', '',        's,t', '', 'r', '',
        's,t', '', 'r', '',        's,t', '', 'r', '',
        's,t', '', 'r', '',        's,t', '', 'r', '',
        's,t', '', 'r', '',        's,t', '', 'r', '',

        's,t', '', 'r', '',        's,t', '', 'r', '',
        's,t', '', 'r', '',        's,t', '', 'r', '',
        's,t', '', 'r', '',        's,t', '', 'r', '',
        's,t', '', 'r', '',        's,t', '', 'r', '',

        'r', '', 'r', '',        's,t', '', 'r', '',
        'r', '', 'r', '',        's,t', '', 'r', '',
        'r', '', 'r', '',        's,t', '', 'r', '',
        'r', '', 'r', '',        's,t', '', 'r', '',

        's,r', '', 'r', '',        's,t', '', 'r', 't',
        's,r', '', 'r', '',        's,t', '', 'r', 't',
        's,r', '', 'r', '',        's,t', '', 'r', 't',
        's,r', '', 'r', '',        's,t', '', 'r', 't',

        't', 't', 's,t', 't',         '', 'r', 's,r', 'r',
        's', 's', 'r,s', 's',         's', 's', 's,r', 'r',
        't', 't', 's,t', 't',         '', 'r', 's,r', 'r',
        's', 's', 'r,s', 's',         's', 's', 's,r', 'r',

        't', 't', 's,t', 't',         '', 'r', 's,r', 'r',
        's', 's', 'r,s', 's',         's', 's', 's,r', 'r',
        't', 't', 's,t', 't',         '', 'r', 's,r', 'r',
        's', 's', 'r,s', 's',         's', 's', 's,r', 'r',

        't', 't', 't', 't',          '', 'r', 's,r', 'r',
        's', 's', 's', 's',          'r', 'r', 'r,t', 't',
        't', 't', 't', 't',          '', 'r', 's,r', 'r',
        's', 's', 's', 's',          'r', 'r', 'r,t', 't',

        't', 't', 't', 't',          '', 'r', 's,r', 'r',
        's', 's', 's', 's',          'r', 'r', 'r,t', 't',
        't', 't', 't', 't',          't', 't', 's,t', 's,t',

        '', '', '', '',         'r', 'r', 'r', '',
    ], 0.19995, -0.013)


def introduce_effect_rhythm():

    ro = GameState.__gsRenderOptions__.transform

    def set_scale(val: float):
        ro.scale = val

    def set_rotate(val: float):
        ro.rotation = val

    def set_overlay(val: float):
        map.overlay_intensity = val

    def set_overlay_move(val: float):
        map.overlay_pos = vec2(val, 0)

    def move_boss(val: float):
        boss.move_speed = val
        boss.reset_state('Walk')

    def scale():
        EasingRunner(0.8, 0.986, 1.0, EaseType.quart).run(set_scale)

    def overlay_shine():
        EasingRunner(0.6, 0.18, 0.25, EaseType.quart).run(set_overlay)

    def rotate_positive():
        EasingRunner(0.4, 1.3, 0.0, EaseType.quart).run(set_rotate)

    def rotate_negative():
        EasingRunner(0.4, -1.3, 0.0, EaseType.quart).run(set_rotate)

    def move_boss_dur():
        EasingRunner(1.6, -4.0, 0.0, EaseType.quad).run(move_boss)

    def move_overlay():
        (EasingRunner(0.8, 0.0, 100.0, EaseType.sine)
         .to(
            0.8, 0.0, EaseType.sine
        ).to(
            0.8, 100.0, EaseType.sine
        ).to(
            0.8, 0.0, EaseType.sine
        ).to(
            0.8, 100.0, EaseType.sine
        ).to(
            0.8, 0.0, EaseType.sine
        ).to(
            0.8, 100.0, EaseType.sine
        ).to(
            0.8, 0.0, EaseType.sine
        ).copy(3).run(set_overlay_move))

    def begin():
        map.player_controllable = True

    register_action('s', Action(scale))
    register_action('rp', Action(rotate_positive))
    register_action('rn', Action(rotate_negative))
    register_action('mv', Action(move_boss_dur))
    register_action('begin', Action(begin))
    register_action('l', Action(overlay_shine))
    register_action('ml', Action(move_overlay))

    rhythm_activate([
        'mv', '', '', '',        '', '', '', '',
        's,begin', '', '', '',        's', '', '', '',
        's', '', '', '',        's', '', '', '',
        's', '', '', '',        's', '', '', '',
        's', '', '', '',        's', '', '', '',
        's', '', 'rp', '',        's', '', 'rn', '',
        's', '', 'rp', '',        's', '', 'rn', '',
        's', '', 'rp', '',        's', '', 'rn', '',
        's', '', 'rp', '',        's', '', 'rn', '',

        'rn', '', 'l,rn', '',        'rn', '', 'l,rn', '',
        'rn', '', 'l,rn', '',        'rn', '', 'l,rn', '',
        'rp', '', 'l,rp', '',        'rp', '', 'l,rp', '',
        'rp', '', 'l,rp', '',        'rp', '', 'l,rp', '',

        'rn', '', 'l,rn', '',        'rn', '', 'l,rn', '',
        'rn', '', 'l,rn', '',        'rn', '', 'l,rn', '',
        'rp', '', 'l,rp', '',        'rp', '', 'l,rp', '',
        'rp', '', 'l,rp', '',        'rp', '', 'l,rp', '',

        'rn,ml', '', 'l,rn', '',        'rn', '', 'l,rn', '',
        'rn', '', 'l,rn', '',        'rn', '', 'l,rn', '',
        'rp', '', 'l,rp', '',        'rp', '', 'l,rp', '',
        'rp', '', 'l,rp', '',        'rp', '', 'l,rp', '',

        'rn', '', 'l,rn', '',        'rn', '', 'l,rn', '',
        'rn', '', 'l,rn', '',        'rn', '', 'l,rn', '',
        'rp', '', 'l,rp', '',        'rp', '', 'l,rp', '',
        'rp', '', 'l,rp', '',        'rp', '', 'l,rp', '',
    ], 0.20)


def generate_effect():
    data = BoolData()
    data.data = True

    def act():
        t = get_music_pos()
        if t > 1.57 and data.data:
            introduce_effect_rhythm()
            introduce_attack_rhythm()
            data.data = False

    instance_create(StableAction(
        1000.0, Action(act)
    ))


class MapTEST1(AutoTileMap):

    def __init__(self):
        global map
        map = self
        super().__init__()
        self.worldPos = vec2(2, 1)

        if TileMap.in_initialize:
            return

        self.savable = False

        self.set_main(FactoryWarn())
        self.ins_group('i', FactoryIron())
        self.ins_obj('1', ObjectLibrary.factory_box0)
        self.ins_obj('fl', ObjectLibrary.fence_l)
        self.ins_obj('fm', ObjectLibrary.fence_m)
        self.ins_obj('fr', ObjectLibrary.fence_r)
        self.ins_obj('p', ObjectLibrary.pointer_1)
        self.ins_obj('s1', ObjectGenerate.make_sign('stand still,\nhold ctrl + s\nto save'))
        self.ins_enemy('g', GunRobot)
        self.ins_obj('c', ObjectGenerate.make_cannon(270, 1.6))
        self.ins_obj('c0', ObjectGenerate.make_cannon(270, 1.6, 0.8))
        self.ins_obj('c1', ObjectGenerate.make_cannon(270, 1.6))
        self.ins_obj('c2', ObjectGenerate.make_cannon(270, 1.6, 0.8))
        self.ins_obj('c3', ObjectGenerate.make_cannon(270, 1.6))
        self.ins_enemy('mr', MeleeRobot)
        self.ins_tile('b', TileLibrary.scaffold)
        self.ins_tile('r', TileLibrary.rail, False)
        self.ins_tile('pn', TileLibrary.pillar, False)
        self.ins_tile('pt', TileLibrary.pillar_top, False)
        self.ins_tile('pc', TileLibrary.pillar_colored, False)
        self.ins_tile('d', TileLibrary.factory_door, False)

        state = BoolData()
        state.data = False

        def activate_boss_1():
            self.player_controllable = False
            play_music('Auroral.mp3', 1.0, 10.0)
            generate_effect()

        def check_door_open():
            pd = get_player_data()
            if pd.player_object.centre.x > 160:
                if not state.data:
                    activate_boss_1()
                state.data = True
            if state.data:
                return False
            return True

        self.ins_tile('D', TileLibrary.make_lock_door(Action(check_door_open)), False)
        self.ins_obj('F', ObjectLibrary.flag)
        self.ins_enemy('B', BossRobot0)
        self.ins_save('*')
        self.generate([
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['i', 'm', 'm', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['i', 'i', 'i', 'r', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', 'D', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'B'],
            ['i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'm', 'm', 'm', 'm', 'm', 'm', 'm'],
        ])
        self.add_background('City2\\1.png', 0, 0.74)
        self.add_background('City2\\2.png', 0.012, 0.87)
        self.add_background('City2\\3.png', 0.036, 0.87)
        self.add_background('City2\\4.png', 0.08, 0.87)
        self.add_background('City2\\5.png', 0.04, 0.87)
        self.add_background('City2\\6.png', 0.02, 0.87)
        self.overlay_image = Texture(load_image('Effects\\Overlay\\red.png'))
        self.bgm = 'STOP'
