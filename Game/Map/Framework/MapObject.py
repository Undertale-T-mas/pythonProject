from Core.Animation.ImageSetBase import ImageSetBase
from Core.GameObject import Entity
from Game.Map.Framework.Tiles import *


class ObjectInfo:
    img_path: str
    on_update: Action | None
    unit_size: vec2 | None
    img_cnt: int
    img_scale: float
    sur_name: str

    def get_image(self) -> ImageSetBase:
        if self.img_cnt == 1:
            res = SingleImage('Objects\\Map\\' + self.img_path)
        else:
            res = ImageSet(self.unit_size, self.unit_size, 'Objects\\Map\\' + self.img_path)
        res.scale = self.img_scale
        return res

    def __init__(self, img_path: str, sur_name: str = 'bg', img_cnt: int = 1, img_scale: float = 1.5, unit_size: vec2 | None = None, on_update: Action | None = None):
        self.img_path = img_path
        self.sur_name = sur_name
        self.on_update = on_update
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
    on_update: Action | None

    def __init__(self, img: ImageSetBase | ObjectInfo | ObjectLibrary, x: int, y: int):
        self.on_update = None
        self.surfaceName = 'bg'
        super().__init__()
        if isinstance(img, ObjectLibrary):
            img = img.value
        if isinstance(img, ObjectInfo):
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
            self.on_update.act()

    def draw(self, render_args: RenderArgs):
        if self.surfaceName == 'bg':
            self.image.draw_self(render_args, self.centre + vec2(0, 48))
        else:
            self.image.draw_self(render_args, self.centre)

