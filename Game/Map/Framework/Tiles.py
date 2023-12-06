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


TILE_LENGTH = 48


class TileInfo:
    imgPath: str
    sizeX: int = 1
    sizeY: int = 1
    bound: CollideRect
    uuid: int
    onUpdate: Action | None = None
    fraction: float = 0.5

    def __init__(self, path: str, size: Tuple[int, int] | List[int], _id: int, on_update: Action = None):
        self.imgPath = path
        self.bound = CollideRect()
        self.bound.area = Rect(0, 0, TILE_LENGTH, TILE_LENGTH)
        self.sizeX = size[0]
        self.sizeY = size[1]
        self.uuid = _id
        self.onUpdate = on_update


class TileLibrary(Enum):
    empty = TileInfo('', [0, 0], 0)
    grass = TileInfo('Tutorial\\Grass.png', [1, 1], 1)


class Tile(Entity, Collidable):
    locX: int = 0
    locY: int = 0

    __areaRect__: Rect

    @property
    def areaRect(self) -> Rect:
        return self.__areaRect__

    @property
    def uuid(self):
        return self.info.uuid

    @property
    def fraction(self):
        return self.info.fraction

    info: TileInfo

    def __init__(self, info: TileInfo | TileLibrary):
        if isinstance(info, TileLibrary):
            info = info.value
        self.physicSurfName = 'tile'
        self.surfaceName = 'tile'
        self.info = info
        self.surfaceName = 'bg'
        if info.imgPath != '':
            self.image = ImageSet(vec2(TILE_LENGTH, TILE_LENGTH), vec2(TILE_LENGTH, TILE_LENGTH), info.imgPath)

    def update(self, args: GameArgs):
        if self.info.onUpdate is not None:
            self.info.onUpdate.act()
        if self.uuid != 0:
            self.centre = vec2((self.locX + 0.5) * TILE_LENGTH, (self.locY + 0.5) * TILE_LENGTH)
            s = CollideRect()
            sz = vec2(TILE_LENGTH, TILE_LENGTH)
            s.area = Rect(self.centre - sz / 2, sz)
            self.physicArea = s
            self.__areaRect__ = s.area

    def draw(self, render_args: RenderArgs):
        if self.image is not None:
            self.image.draw_self(render_args, self.centre)
