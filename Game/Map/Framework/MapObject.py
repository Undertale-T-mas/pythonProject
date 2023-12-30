import core
from Core.GameStates import GameState
from Game.Map.Objects.Cannon import Cannon
from Game.Map.Objects.Crystal import *
from Game.Map.Objects.ObjectBase import *
from core import *

from Game.Components.Readable import *
from Game.Components.Readable import PanelText
from Game.Map.Framework.Tiles import *


class ObjectInfo:
    img_path: str
    on_update: EntityEvent | None
    unit_size: vec2 | None
    img_cnt: int
    img_scale: float
    sur_name: str
    on_create: ArgAction | None
    img_anchor: vec2 | None

    def get_image(self) -> ImageSetBase:
        if self.img_cnt == 1:
            res = SingleImage('Objects\\Map\\' + self.img_path)
        else:
            res = ImageSet(self.unit_size, self.unit_size, 'Objects\\Map\\' + self.img_path)
        res.scale = self.img_scale
        return res

    def __init__(self, img_path: str, sur_name: str = 'bg', img_cnt: int = 1, img_scale: float = 1.5, anchor: vec2 | None = None,
                 unit_size: vec2 | None = None, on_create: ArgAction | None = None, on_update: EntityEvent | None = None):
        self.img_path = img_path
        self.img_anchor = anchor
        self.sur_name = sur_name
        self.on_update = on_update
        self.on_create = on_create
        self.img_scale = img_scale
        self.img_cnt = img_cnt
        self.unit_size = unit_size


class ObjectLibrary(Enum):
    factory_box0 = ObjectInfo('Box0.png')
    factory_box1 = ObjectInfo('Box1.png')
    factory_box2 = ObjectInfo('Box2.png')
    factory_box3 = ObjectInfo('Box3.png')
    factory_box4 = ObjectInfo('Box4.png')
    fence_l = ObjectInfo('FenceL.png', 'default')
    fence_m = ObjectInfo('FenceM.png', 'default')
    fence_r = ObjectInfo('FenceR.png', 'default')
    pointer_1 = ObjectInfo('Pointer1.png', img_scale=2)
    pointer_2 = ObjectInfo('Pointer2.png', img_scale=2)
    locker = ObjectInfo('Locker.png')
    flag = ObjectInfo('Flag.png', anchor=vec2(16, 16))
    barrel_0 = ObjectInfo("Barrel0.png")
    barrel_1 = ObjectInfo("Barrel1.png")


class MapObject(Entity):
    on_update: EntityEvent | None

    def __init__(self, img: ImageSetBase | ObjectInfo | ObjectLibrary, x: int, y: int):
        self.on_update = None
        self.surfaceName = 'bg'
        super().__init__()
        if isinstance(img, ObjectLibrary):
            img = img.value
        anchor = None
        if isinstance(img, ObjectInfo):
            if img.on_create is not None:
                img.on_create.act(x, y)
            self.on_update = img.on_update
            self.surfaceName = img.sur_name
            anchor = img.img_anchor
            img = img.get_image()

        self.image = img
        if isinstance(anchor, vec2):
            self.image.anchor = ACustom(anchor)
        self.centre = vec2((x + 0.5) * TILE_LENGTH, (y + 1) * TILE_LENGTH - img.blockSize.y * img.scale * 0.5)

    @property
    def need_update(self):
        return self.on_update is not None

    def update(self, args: GameArgs):
        if self.on_update is not None:
            self.on_update.act(self)

    def draw(self, render_args: RenderArgs):
        if self.surfaceName == 'bg':
            self.image.draw_self(render_args, self.centre + vec2(0, 48))
        else:
            self.image.draw_self(render_args, self.centre)


class ObjectGenerate:
    class PanelData:
        ins: PanelText

        def set_text(self, pos: vec2, text: str):
            self.ins = PanelText(text, pos)

    class ObjectTempData:
        ins: MapObjectFuncBase

    @staticmethod
    def make_sign(info: str):
        u = ObjectGenerate.PanelData()

        def sign_test(obj1: Entity):
            obj2 = GameState.__gsScene__.__player__
            pos1 = vec2(obj1.centre.x, obj1.centre.y / 1.3)
            pos2 = vec2(obj2.centre.x, obj2.centre.y / 1.3 + 24)

            if (pos1 - pos2).length_squared() <= 5000.0:
                u.ins.appear()
            else:
                u.ins.disappear()

        def sign_create(x: int, y: int):
            u.set_text(vec2((x + 0.5) * TILE_LENGTH, (y + 0.5) * TILE_LENGTH), info)
            instance_prepare(u.ins)

        return ObjectInfo('Sign.png', on_create=ArgAction(sign_create), on_update=EntityEvent(sign_test))

    @staticmethod
    def make_crystal(map_world_pos: vec2, uuid: int, data: Any = None):
        u = ObjectGenerate.ObjectTempData()
        u.ins = SaveCrystal(map_world_pos, uuid, data)

        def on_update(obj1: Entity):
            u.ins.on_update(obj1)

        def on_create(x: int, y: int):
            u.ins.on_create(x, y)
            instance_prepare(u.ins)

        return ObjectInfo('SaveCrystal.png', on_create=ArgAction(on_create), on_update=EntityEvent(on_update),
                          img_cnt=8, unit_size=vec2(32, 32))

    @staticmethod
    def make_cannon(direction: float, interval: float, delay: float = 0.0):
        u = ObjectGenerate.ObjectTempData()
        u.ins = Cannon(direction, interval, delay=delay)

        def on_update(obj1: Entity):
            u.ins.on_update(obj1)

        def on_create(x: int, y: int):
            u.ins.on_create(x, y)
            instance_prepare(u.ins)

        return ObjectInfo('Cannon.png', on_create=ArgAction(on_create), on_update=EntityEvent(on_update), anchor=vec2(13, 13))

