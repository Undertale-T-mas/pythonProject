from core import *
from map import *


class MapTEST1(AutoTileMap):
    class BoolData:
        data: bool

    def __init__(self):
        super().__init__()
        self.worldPos = vec2(1, 1)

        if TileMap.in_initialize:
            return

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

        state = MapTEST1.BoolData()
        state.data = False

        def check_door_open():
            pd = get_player_data()
            if pd.player_object.centre.x > 900:
                state.data = True
            if state.data:
                return True
            return False

        self.ins_tile('D', TileLibrary.make_lock_door(Action(check_door_open)), False)
        self.ins_obj('F', ObjectLibrary.flag)
        self.ins_save('*')
        self.generate([
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['i', 'r', 'r', 'm','m,c','m,c0','m,c1','m,c2','m,c3','m','0','0','0', '*', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['i', 'r', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'D'],
            ['0', '0', '0', '0', '*', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'm', 'm', 'm', 'm'],
        ])
        self.add_background('City\\1.png', 0, 0.74)
        self.add_background('City\\2.png', 0.012, 0.87)
        self.add_background('City\\3.png', 0.036, 0.87)
        self.add_background('City\\4.png', 0.08, 0.87)
        self.overlay_image = Texture(load_image('Effects\\Overlay\\purple.png'))
        self.bgm = 'STOP'
