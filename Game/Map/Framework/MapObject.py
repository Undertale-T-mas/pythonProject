import core
from Core.GameStates import GameState
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

    def get_image(self) -> ImageSetBase:
        if self.img_cnt == 1:
            res = SingleImage('Objects\\Map\\' + self.img_path)
        else:
            res = ImageSet(self.unit_size, self.unit_size, 'Objects\\Map\\' + self.img_path)
        res.scale = self.img_scale
        return res

    def __init__(self, img_path: str, sur_name: str = 'bg', img_cnt: int = 1, img_scale: float = 1.5,
                 unit_size: vec2 | None = None, on_create: ArgAction | None = None, on_update: EntityEvent | None = None):
        self.img_path = img_path
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
    pointer_1 = ObjectInfo('Pointer1.png')
    pointer_2 = ObjectInfo('Pointer2.png')
    locker = ObjectInfo('Locker.png')
    flag = ObjectInfo('Flag.png')
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
        if isinstance(img, ObjectInfo):
            if img.on_create is not None:
                img.on_create.act(x, y)
            self.on_update = img.on_update
            self.surfaceName = img.sur_name
            img = img.get_image()

        self.image = img
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
