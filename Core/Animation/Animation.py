from Core.Animation.ImageSetBase import ImageSetBase
from Core.GameArgs import GameArgs
from Core.GameObject import Entity
from pygame import Vector2 as vec2


class Animation(Entity):
    __interval__: float
    __autoDispose__: bool

    def __init__(self, img: ImageSetBase, interval: float, centre: vec2, auto_dispose: bool = True):
        super().__init__()
        self.image = img
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