from Core.Animation.Anchor import *
from Core.Animation.AnchorBase import *
from Core.Animation.ImageSetBase import *
from Core.Animation.ImageSet import *
import Core.GameStates.GameStates
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

from Game.Map.Framework.TileMap import *


class MapTEST0(TileMap):
    def __init__(self):
        super().__init__()
        self.set_tile(2,5, Tile(TileLibrary.grass))
        self.set_tile(3,5, Tile(TileLibrary.grass))
        self.set_tile(4,5, Tile(TileLibrary.grass))