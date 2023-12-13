from Core.Animation.Anchor import *
from Core.Animation.AnchorBase import *
from Core.Animation.ImageSetBase import *
from Core.Animation.ImageSet import *
import Core.GameStates.GameState
from Core.GameStates.ObjectManager import *
from Core.Physics.PhysicSurface import *
from Core.Physics.PhysicManager import *
from Core.Physics.Collidable import *
from Core.Physics.CollidingArea import *
from Core.Render.RenderOptions import *
from Core.Render.SurfaceManager import *
from Core.Render.VSurface import *
from Core.GameObject import *
from Core.GameArgs import *
from pygame import Vector2 as vec2
from pygame import *

from Game.Characters.Enemys.Robots import *
from Game.Map.Framework.MapGenerate import *
from Game.Map.Framework.MapObject import ObjectLibrary
from Game.Map.Framework.TileMap import *


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
        self.generate([
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['M', 'M', 'M', 'M', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'fl','fm','fm','fr', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['M', 'M', 'M', 'M', '0', '0', '0', '0', '0', '0', '0', '0', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '0', '0'],
            ['M', 'M', 'M', 'M', 'i', 'i', 'i', 'i', 'i', '0', '0', '0', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', '0', '0'],
            ['M', 'M', 'M', 'M', 'i', 'i', 'i', 'i', 'i', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ])
        self.add_background('City\\1.png', 0, 0.64)
        self.add_background('City\\2.png', 0.012, 0.7)
        self.add_background('City\\3.png', 0.036, 0.7)
        self.add_background('City\\4.png', 0.08, 0.7)
        self.add_object(GunRobot(14, 0))
