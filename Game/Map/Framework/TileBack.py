from Core.GameObject import *
from Core.GameStates import GameState


class TileBack(Entity):
    __moveXFactor__: float
    __follow__: Entity

    def __init__(self, move_x_factor, img: ImageSetBase):
        super().__init__()
        self.__moveXFactor__ = move_x_factor
        self.image = img
        self.image.stable = True
        self.__follow__ = None
        self.image.scale = GameState.__gsRenderOptions__.screenSize.y / self.image.imageSource.get_height()

    def update(self, args: GameArgs):
        if self.__follow__ is None:
            self.__follow__ = GameState.__gsScene__.camera
        full = GameState.__gsRenderOptions__.screenSize
        xc = full.x / 2
        self.centre = vec2(xc + self.__moveXFactor__ * (self.__follow__.centre.x - xc), full.y * 0.5)

    def draw(self, render_args: RenderArgs):
        super().draw(render_args)