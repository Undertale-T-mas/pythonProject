from Core.GameStates.Scene import *
from Core.GameStates import *
from Game.Characters.Humans.Player import Player
from Game.Map.Framework.TileMap import *
from Game.Scenes.TileMapScene import *


class FightScene(TileMapScene):
    __phyManager__: PhysicManager
    __player__: Player

    @property
    def player(self):
        return self.__player__

    def __init__(self):
        super().__init__()
        self.__phyManager__ = PhysicManager()

    def create_player(self):
        self.__player__ = Player()
        Core.GameStates.GameStates.instance_create(self.__player__)

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.__phyManager__.update()

    def instance_create(self, obj: GameObject):
        super().instance_create(obj)
        if isinstance(obj, Collidable):
            self.__phyManager__.insert_object(obj)
        self.__phyManager__.check('player', 'barrage')
        self.__phyManager__.check('pl_bullet', 'enemy')

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager)
        rec = pygame.rect.Rect(0, 0, self.__render_options__.screenSize.x, self.__render_options__.screenSize.y)
        surface_manager.screen.blit(
            surface_manager.get_surface('bg'),
            dest=rec,
            area=rec,
        )
        surface_manager.screen.blit(
            surface_manager.get_surface('default'),
            dest=rec,
            area=rec,
        )
        if surface_manager.exist_surface('barrage'):
            surface_manager.screen.blit(
                surface_manager.get_surface('barrage'),
                dest=rec,
                area=rec,
            )

