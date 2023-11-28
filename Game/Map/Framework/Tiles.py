from enum import Enum

from Core.Animation.Anchor import *
from Core.Animation.AnchorBase import *
from Core.Animation.ImageSetBase import *
from Core.Animation.ImageSet import *
from Core.GameStates.Scene import *
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


class TileInfo:
    imgPath: str
    sizeX: int = 1
    sizeY: int = 1
    _id: int

    def __init__(self, path: str, size: Tuple[int, int] | List[int], _id: int):
        self.imgPath = path
        self.sizeX = size[0]
        self.sizeY = size[1]
        self._id = _id


class TileLibrary(Enum):
    empty = TileInfo('', [0, 0], 0)
    grass = TileInfo('Tutorial\\Grass.png', [1, 1], 1)


class Tile(Entity, Collidable):
    locX: int
    locY: int

    info: TileInfo

    def __init__(self, info: TileInfo):
        self.physicSurfName = 'tile'
        self.surfaceName = 'tile'
        self.info = info
