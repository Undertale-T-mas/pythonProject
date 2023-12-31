from core import *
from map import *


class MapTEST1(AutoTileMap):
    def __init__(self):
        super().__init__()
        self.worldPos = vec2(0, -1)

        if TileMap.in_initialize:
            return

        self.set_main(FactoryWarn())
        self.ins_group('i', FactoryIron())
        self.ins_obj('1', ObjectLibrary.factory_box0)
        self.ins_obj('fl', ObjectLibrary.fence_l)
        self.ins_obj('fm', ObjectLibrary.fence_m)
        self.ins_obj('fr', ObjectLibrary.fence_r)
        self.ins_obj('p', ObjectLibrary.pointer_1)
        self.ins_obj('s1', ObjectGenerate.make_sign('press r\nto reload'))
        self.ins_enemy('g', GunRobot)
        self.ins_enemy('mr', MeleeRobot)
        self.ins_tile('b', TileLibrary.scaffold)
        self.ins_tile('r', TileLibrary.rail, False)
        self.ins_tile('pn', TileLibrary.pillar, False)
        self.ins_tile('pt', TileLibrary.pillar_top, False)
        self.ins_tile('pc', TileLibrary.pillar_colored, False)
        self.ins_tile('d', TileLibrary.factory_door, False)
        self.generate([
            ['M', 'M', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', '0', '0', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'M', 'M'],
            ['M', 'M', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'M', 'M'],
            ['M', 'M', '0', '0', '0', 'd', '0', '0', '0', 'i', 'i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'M', 'M'],
            ['M', 'M', '0', '0', 's1','0', '0', '0', '0', 'i', 'i', 'r', 'r', '0', '0', 'r', 'r', 'r', 'i', 'i', 'i', 'r', 'r', 'r', 'M', 'M'],
            ['M', 'M', 'r', 'r', 'M', 'M', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i', 'i', 'i', '0', '0', '0', 'M', 'M'],
            ['0', '0', '0', '0', 'M', 'M', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i', 'i', 'i', '0', '0', '0', 'M', 'M'],
            ['0', 'fl','fm','fr,1','M','M','0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'i', 'i', '0', '0', '0', 'r', 'M', 'M'],
            ['M', 'M', 'b', 'M', 'M', 'M', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'd', '0', '0', '0', '0', '0', 'M', 'M'],
            ['M', 'M', 'M', 'M', 'M', 'M', '0', '0', '0', 'p','fl','fr', '0', '0', '0', '0', 'mr','0', '0', '0', '0', '0', '0', '0', 'M', 'M'],
            ['0', '0', '0', '0', 'M', 'M', '0', '0', '0', 'i', 'i', 'i', '0', '0', 'i', 'i', 'i', '0', 'i', 'i', 'i', '0', '0', 'g', 'M', 'M'],
            ['0', '0', '0', '0', 'M', 'M', '0', '0', '0', 'i', 'i', 'i', '0', '0', 'i', 'i', 'i', '0', 'i', 'i', 'i', 'M', 'M', 'M', 'M', 'M'],
        ])
        self.add_background('City\\1.png', 0, 0.74)
        self.add_background('City\\2.png', 0.012, 0.87)
        self.add_background('City\\3.png', 0.036, 0.87)
        self.add_background('City\\4.png', 0.08, 0.87)
        self.overlay_image = Texture(load_image('Effects\\Overlay\\purple.png'))
        self.bgm = 'Expedition.mp3'
