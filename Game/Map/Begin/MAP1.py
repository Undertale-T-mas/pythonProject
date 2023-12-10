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

from Game.Characters.Enemys.Robots import MeleeRobot
from Game.Map.Framework.TileMap import *


class MapTEST0(TileMap):
    def __init__(self):
        super().__init__()
        self.worldPos = vec2(0, -1)

        if TileMap.in_initialize:
            return

        self.set_tile(0, 5, Tile(TileLibrary.grass))
        self.set_tile(1, 5, Tile(TileLibrary.grass))
        self.set_tile(3, 9, Tile(TileLibrary.grass))
        self.set_tile(4, 9, Tile(TileLibrary.grass))
        self.set_tile(6, 4, Tile(TileLibrary.grass))
        self.set_tile(7, 4, Tile(TileLibrary.grass))
        self.set_tile(6, 7, Tile(TileLibrary.grass))
        self.set_tile(7, 7, Tile(TileLibrary.grass))
        self.set_tile(9, 1, Tile(TileLibrary.grass))
        self.set_tile(10, 1, Tile(TileLibrary.grass))
        self.set_tile(12, 9, Tile(TileLibrary.dirt_l))
        self.set_tile(12, 8, Tile(TileLibrary.dirt_l))
        self.set_tile(12, 7, Tile(TileLibrary.dirt_l))
        self.set_tile(12, 6, Tile(TileLibrary.dirt_l))
        self.set_tile(12, 5, Tile(TileLibrary.grass_cl))
        self.set_tile(14, 10, Tile(TileLibrary.iron_cl))
        self.set_tile(15, 10, Tile(TileLibrary.iron_t))
        self.set_tile(16, 10, Tile(TileLibrary.iron_t))
        self.set_tile(17, 10, Tile(TileLibrary.iron_cr))
        self.set_tile(14, 11, Tile(TileLibrary.iron_l))
        self.set_tile(15, 11, Tile(TileLibrary.iron_inner))
        self.set_tile(16, 11, Tile(TileLibrary.iron_inner))
        self.set_tile(17, 11, Tile(TileLibrary.iron_r))
        self.add_background('City\\1.png', 0, 0.64)
        self.add_background('City\\2.png', 0.02)
        self.add_background('City\\3.png', 0.06)
        self.add_background('City\\4.png', 0.2)
        self.add_object(MeleeRobot(14, 0))
        self.add_object(MeleeRobot(4, 0))
        self.add_object(MeleeRobot(10, 0))

