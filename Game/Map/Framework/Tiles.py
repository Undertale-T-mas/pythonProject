from enum import Enum

from Core.Animation.Anchor import *
from Core.Animation.AnchorBase import *
from Core.Animation.ImageSetBase import *
from Core.Animation.ImageSet import *
from Core.GameStates.Scene import *
import Core.GameStates.GameState
from Core.GameStates.ObjectManager import *
from Core.MathUtil import FRect
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
    onUpdate: Action | None
    fraction: float = 0.5
    collidable: bool = True
    __img__: ImageSet | None

    @property
    def img(self) -> ImageSet:
        if self.imgPath != '' and self.__img__ is None:
            self.__img__ = ImageSet(vec2(TILE_LENGTH, TILE_LENGTH), vec2(TILE_LENGTH, TILE_LENGTH), 'Tiles\\' + self.imgPath)
            sz = self.__img__.imageSource.get_size()
            sz = vec2(sz[0], sz[1])
            mod = vec2(sz.x % 48, sz.y % 48)
            if mod.x != 0 or mod.y != 0:
                if sz.y < 48:
                    scale = 48 / sz.y
                    self.__img__.__imageSource__ = pygame.transform.scale(
                        self.__img__.imageSource, vec2(scale * sz.x, scale * sz.y)
                    )
        return self.__img__

    def __init__(self, path: str, size: FRect, _id: int, collidable: bool = True, on_update: Action = None):
        self.imgPath = path
        self.bound = CollideRect()
        self.bound.area = FRect(TILE_LENGTH * size.x, TILE_LENGTH * size.y, TILE_LENGTH * size.width, TILE_LENGTH * size.height)
        self.sizeX = int(size.right)
        self.sizeY = int(size.bottom)
        self.uuid = _id
        self.__img__ = None
        self.collidable = collidable
        self.onUpdate = on_update


class TileLibrary(Enum):
    empty = TileInfo('', size=FRect(0, 0, 1, 1), _id=0, collidable=False)
    grass = TileInfo('Tutorial\\Grass.png', size=FRect(0, 0, 1, 1), _id=1)
    grass_cl = TileInfo('Tutorial\\GrassCL.png', size=FRect(0.1, 0, 0.9, 1), _id=2)
    grass_cr = TileInfo('Tutorial\\GrassCR.png', size=FRect(0, 0, 0.9, 1), _id=3)
    dirt = TileInfo('Tutorial\\Dirt.png', size=FRect(0, 0, 1, 1), _id=4)
    dirt_l = TileInfo('Tutorial\\DirtL.png', size=FRect(0.1, 0, 0.9, 1), _id=5)
    dirt_r = TileInfo('Tutorial\\DirtR.png', size=FRect(0, 0, 0.9, 1), _id=6)
    iron_cl = TileInfo('Factory\\IronCL.png', size=FRect(0, 0, 1, 1), _id=7)
    iron_cr = TileInfo('Factory\\IronCR.png', size=FRect(0, 0, 1, 1), _id=8)
    iron_t = TileInfo('Factory\\IronT.png', size=FRect(0, 0, 1, 1), _id=9)
    iron_l = TileInfo('Factory\\IronL.png', size=FRect(0, 0, 1, 1), _id=10)
    iron_r = TileInfo('Factory\\IronR.png', size=FRect(0, 0, 1, 1), _id=11)
    iron_inner = TileInfo('Factory\\IronInner.png', size=FRect(0, 0, 1, 1), _id=12)
    purple_pure = TileInfo('Factory\\PurePurple.png', size=FRect(0, 0, 1, 1), _id=13)
    purple_streak = TileInfo('Factory\\StreakPurple.png', size=FRect(0, 0, 1, 1), _id=14)
    warn_cl = TileInfo('Factory\\WarnCL.png', size=FRect(0, 0, 1, 1), _id=7)
    warn_cr = TileInfo('Factory\\WarnCR.png', size=FRect(0, 0, 1, 1), _id=8)
    warn_t = TileInfo('Factory\\WarnT.png', size=FRect(0, 0, 1, 1), _id=9)
    warn_l = TileInfo('Factory\\WarnL.png', size=FRect(0, 0, 1, 1), _id=10)
    warn_r = TileInfo('Factory\\WarnR.png', size=FRect(0, 0, 1, 1), _id=11)


class Tile(Entity, Collidable):
    locX: int = 0
    locY: int = 0

    __areaRect__: FRect

    @staticmethod
    def Empty():
        return Tile(TileLibrary.empty)

    @property
    def areaRect(self) -> FRect:
        return self.__areaRect__

    @property
    def uuid(self):
        return self.info.uuid

    @property
    def collidable(self):
        return self.info.collidable

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
        self.image = info.img

    def update(self, args: GameArgs):
        if self.info.onUpdate is not None:
            self.info.onUpdate.act()
        if self.uuid != 0:
            self.centre = vec2((self.locX + 0.5) * TILE_LENGTH, (self.locY + 0.5) * TILE_LENGTH)
            s = CollideRect()
            s.area = FRect(
                self.locX * TILE_LENGTH + self.info.bound.area.x,
                self.locY * TILE_LENGTH + self.info.bound.area.y,
                self.info.bound.area.width,
                self.info.bound.area.height
            )
            self.physicArea = s
            self.__areaRect__ = s.area

    def draw(self, render_args: RenderArgs):
        if self.image is not None:
            self.image.draw_self(render_args, self.centre)
