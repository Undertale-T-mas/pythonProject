from Core.Profile.Savable import *
from Game.Map.Framework.Tiles import *
from core import *
from Game.Map.Objects.ObjectBase import MapObjectFuncBase


class SaveCrystal(MapObjectFuncBase):

    centre: vec2
    visible: Savable[bool]
    time: float
    time_tot: float

    def on_update(self, object_source: Entity):
        object_source.visible = self.visible.value
        object_source.centre = self.centre + vec2(0, -24 - Math.sin_deg(self.time_tot * 90) * 15)
        if self.time >= 0.1:
            self.time -= 0.1
            MapObjectFuncBase.image_changed()
            object_source.image.indexX += 1
            if object_source.image.indexX == 8:
                object_source.image.indexX = 0

    def on_create(self, pos_x: int, pos_y: int):
        self.centre = vec2((0.5 + pos_x) * TILE_LENGTH, (0.5 + pos_y) * TILE_LENGTH)
        self.visible = Savable(self.save_path() + '.' + 'vis', True, True)

    def __init__(self, world_pos: vec2, id: int):
        super().__init__(world_pos, id)
        self.time = 0
        self.time_tot = 0

    def update(self, args: GameArgs):
        self.time += args.elapsedSec
        self.time_tot += args.elapsedSec
