from Core.GameStates.Scene import *
from Game.Map.Framework.TileMap import *


class FightScene(Scene):
    tileMap: TileMap

    def __init__(self):
        super().__init__()

    def set_tiles(self, tile_map: TileMap):
        self.tileMap = tile_map
        self.instance_create(self.tileMap)

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager)
        rec = pygame.rect.Rect(0, 0, self.__render_options__.screenSize.x, self.__render_options__.screenSize.y)
        surface_manager.screen.blit(
            surface_manager.get_surface('default'),
            dest=rec,
            area=rec,
        )

