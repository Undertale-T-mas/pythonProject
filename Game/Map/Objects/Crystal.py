from Core.Profile.Savable import *
from Game.Map.Framework.Tiles import *
from Resources.ResourceLib import Sounds
from core import *
from Game.Map.Objects.ObjectBase import MapObjectFuncBase


class SaveCrystal(MapObjectFuncBase):

    centre: vec2
    visible: Savable[bool]
    time: float
    time_tot: float
    data: Any

    def on_update(self, object_source: Entity):
        if object_source.is_disposed():
            raise ArgumentError()

        object_source.visible = self.visible.value
        object_source.centre = self.centre + vec2(0, -24 - Math.sin_deg(self.time_tot * 90) * 15)
        if self.time >= 0.1:
            self.time -= 0.1
            MapObjectFuncBase.image_changed()
            object_source.image.indexX += 1
            if object_source.image.indexX == 8:
                object_source.image.indexX = 0

        player = MapObjectFuncBase.get_player()

        if not player.save_slot_acceptable():
            return

        delta = player.centre - object_source.centre
        delta.y /= 2

        if delta.length_squared() <= 35 * 35:
            # touched player
            object_source.dispose()
            img = object_source.image.copy()
            instance_create(ShardAnimation(
                img, object_source.centre + vec2(0, 48), FRect(0.5, 0, 0.5, 0.5),
                vec2(2.2, -4), 17.5, 1.5, 12.0,  'bg'
            ))
            instance_create(ShardAnimation(
                img.copy(), object_source.centre + vec2(0, 48), FRect(0, 0.5, 0.5, 0.5),
                vec2(-2.2, 4), 17.5, 1.5, 12.0, 'bg'
            ))
            self.dispose()
            player.gather_save()
            instance_create(
                Animation(
                    ImageSet(vec2(48, 48), vec2(48, 48), 'Effects\\Crystal\\default.png'),
                    0.06,
                    object_source.centre + vec2(0, 48),
                    scale=2.0,
                    surf_name='bg'
                )
            )
            anim_set2 = ImageSet(vec2(48, 48), vec2(48, 48), 'Effects\\Crystal\\default.png')
            anim_set2.alpha = 0.675
            anim_set2.flip = True
            Sounds.crystal.play()
            instance_create(Animation(anim_set2, 0.07, object_source.centre + vec2(0, 48), scale=2.7, surf_name='bg')) 
            self.image_changed()
            instance_create(StableAction(0.5, action=Action(self.image_changed)))
            self.visible.value = False

    def on_create(self, pos_x: int, pos_y: int):
        self.centre = vec2((0.5 + pos_x) * TILE_LENGTH, (0.5 + pos_y) * TILE_LENGTH)
        self.visible = Savable(self.save_path() + '.' + 'vis', True, True)

    def __init__(self, world_pos: vec2, _id: int, data: Any = None):
        super().__init__(world_pos, _id)
        self.time = 0
        self.data = data
        self.time_tot = 0

    def update(self, args: GameArgs):
        self.time += args.elapsedSec
        self.time_tot += args.elapsedSec
