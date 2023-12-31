import core

from Game.Characters.Enemys.Robots import *
from Game.Map.Framework.MapGenerate import *
from Game.Map.Framework.MapObject import *
from Game.Map.Framework.TileMap import *

import map


class MapTEST0(AutoTileMap):
    def __init__(self):
        super().__init__()
        self.worldPos = vec2(-1, -1)

        if TileMap.in_initialize:
            return

        self.set_main(FactoryWarn())
        self.ins_group('i', FactoryIron())
        self.ins_obj('1', ObjectLibrary.factory_box0)
        self.ins_obj('fl', ObjectLibrary.fence_l)
        self.ins_obj('fm', ObjectLibrary.fence_m)
        self.ins_obj('fr', ObjectLibrary.fence_r)
        self.ins_obj('s1', ObjectGenerate.make_sign('press arrow\nkey or A&D\nto move'))
        self.ins_obj('s2', ObjectGenerate.make_sign('press c or w or\nor UP to jump'))
        self.ins_obj('s3', ObjectGenerate.make_sign('press spacebar\nor j to shoot'))
        self.ins_enemy('g', GunRobot)
        self.ins_tile('b', TileLibrary.scaffold)
        self.ins_tile('.', TileLibrary.iron_bg, False, True)
        self.ins_tile('pn', TileLibrary.pillar, False)
        self.ins_tile('pt', TileLibrary.pillar_top, False)
        self.ins_tile('pc', TileLibrary.pillar_colored, False)
        self.ins_tile('d', TileLibrary.factory_door, False, False)
        self.generate([
            ['M', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'M', 'M', 'M'],
            ['M', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'M', 'M', 'M'],
            ['M', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'M', 'M'],
            ['M', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'M', 'M'],
            ['M', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'M', 'M'],
            ['M', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'pt','0', '0', '0', '0', '0', '0', 'd', '0'],
            ['M', 's1','1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'pn','0', '0', '0', 'g', '0', '0', '0', '0'],
            ['M', 'M', 'M', 'M', '0', '0', '0', '0', '0', '0', '0', '0', 's3','fl','fm','fm','fr','pc','0', '0', 'M', 'M', 'M', 'M', 'M', 'M'],
            ['M', 'M', 'M', 'M', '0','s2', '0', '0', '0', '0', '0', '0', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M'],
            ['M', 'M', 'M', 'M', 'i', 'i', 'b', 'b', 'i', '0', '0', '0', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '0', '0'],
            ['M', 'M', 'M', 'M', 'i', 'i', 'i', 'i', 'i', '0', '0', '0', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '0', '0'],
        ])
        self.add_background('City\\1.png', 0, 0.74)
        self.add_background('City\\2.png', 0.012, 0.87)
        self.add_background('City\\3.png', 0.036, 0.87)
        self.add_background('City\\4.png', 0.08, 0.87)
        self.overlay_image = Texture(load_image('Effects\\Overlay\\purple.png'))
        self.bgm = 'Expedition.mp3'
