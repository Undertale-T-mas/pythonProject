from Core.Animation.ImageSetBase import ImageSetBase
from Core.GameArgs import GameArgs, RenderArgs
from Core.Entity import Entity
from Core.MathUtil import *


class Animation(Entity):
    __interval__: float
    __autoDispose__: bool

    def __init__(self,
                 img: ImageSetBase, interval: float,
                 centre: vec2, auto_dispose: bool = True,
                 surf_name: str = 'default',
                 scale: float | None = None
                 ):
        super().__init__()
        self.image = img
        if scale is not None:
            self.image.scale = scale
        self.surfaceName = surf_name
        self.image.indexX = 0
        self.__interval__ = interval
        self.centre = centre
        self.tot = 0
        self.__autoDispose__ = auto_dispose
        self.end = False

    tot: float
    end: bool

    def update(self, args: GameArgs):
        if self.end:
            return

        self.tot += args.elapsedSec
        if self.tot >= self.__interval__:
            self.tot -= self.__interval__
            self.image.indexX += 1
            if self.image.source_area().right > self.image.imageSource.get_size()[0]:
                if self.__autoDispose__:
                    self.dispose()
                else:
                    self.image.indexX -= 1
                    self.end = True


class AlphaAnimation(Animation):
    alphaDecrease: float

    def __init__(self, img: ImageSetBase, interval: float, centre: vec2, alpha_decrease: float):
        super().__init__(img, interval, centre, False)
        self.alphaDecrease = alpha_decrease

    def update(self, args: GameArgs):
        super().update(args)
        if self.end:
            self.image.alpha -= self.alphaDecrease * args.elapsedSec * 62.5
            if self.image.alpha < 0:
                self.dispose()


class ShardAnimation(Entity):
    fade_speed: float
    speed: vec2
    scale_speed: float

    def __init__(self, img: ImageSetBase, centre: vec2, area: FRect, speed: vec2, fade_speed: float, scale: float | vec2 | None = None, scale_speed: float = 12.0, surf_name: str = 'default'):
        super().__init__()
        self.speed = speed
        self.scale_speed = scale_speed
        if scale is None:
            scale = img.scale
        if isinstance(scale, float):
            scale = vec2(scale, scale)
        self.scale_speed = self.scale_speed * scale
        self.surfaceName = surf_name
        img.scale = scale
        self.fade_speed = fade_speed
        self.centre = (centre +
                       vec2((area.x + area.width / 2 - 0.5) * img.blockSize.x * scale.x,
                            (area.y + area.height / 2 - 0.5) * img.blockSize.y * scale.y)
                       )
        self.image = img
        sz = self.image.blockSize.copy()
        self.image.blockSize.x = area.width * sz.x
        self.image.blockSize.y = area.height * sz.y
        self.image.offset = vec2(area.x * sz.x, area.y * sz.y)
        self.alpha = 1.0

    alpha: float

    def update(self, args: GameArgs):
        self.centre += self.speed * args.elapsedSec * 60
        self.alpha -= self.fade_speed * args.elapsedSec
        self.image.alpha = self.alpha
        self.image.__scale__ = self.image.__scale__ + self.scale_speed * args.elapsedSec

        if self.alpha <= 0:
            self.dispose()

    def draw(self, render_args: RenderArgs):
        super().draw(render_args)
