from Core.Animation.Animation import Animation
from Core.GameStates.Scene import *
from Core.GameStates import *
import Core.GameStates.GameState
from Core.GameStates.GameState import *
from Game.Characters.Humans.Player import Player
from Game.Characters.Movable import DeathAnimation
from Game.Map.Framework.TileMap import *
from Game.Scenes.TileMapScene import *


class FightCameraObj(Entity):
    __player__: Entity
    __map__: TileMap

    def __init__(self, player: Entity, map: TileMap):
        super().__init__()
        self.__player__ = player
        self.__map__ = map
        self.centre = GameState.__gsRenderOptions__.screenSize / 2

    def calc_x(self):
        screen_x = GameState.__gsRenderOptions__.screenSize.x
        map_w = self.__map__.width * TILE_LENGTH
        if map_w <= screen_x:
            return screen_x / 2
        else:
            raise Exception()

    def calc_y(self):
        screen_y = GameState.__gsRenderOptions__.screenSize.y
        map_h = self.__map__.height * TILE_LENGTH
        if map_h <= screen_y:
            return screen_y / 2
        else:
            raise Exception()

    def update(self, args: GameArgs):
        self.centre.x = self.calc_x()
        self.centre.y = self.calc_y()

    def draw(self, render_args: RenderArgs):
        pass


class FightScene(TileMapScene):

    __phyManager__: PhysicManager
    __player__: Player

    @property
    def player(self):
        return self.__player__

    def __init__(self):
        super().__init__()
        self.__phyManager__ = PhysicManager()

    def __move_player__(self):
        self.__player__.centre = vec2(-1000, -1000)

    def remove_player(self):
        self.__player__.dispose()
        self.instance_create(DelayedAction(0, Action(self.__move_player__)))
        self.__player__.image.imageSource = self.player.__image_set__.imageDict['Punk_death']
        self.instance_create(DeathAnimation(self.__player__.image, self.__player__, vec2(20, 30), vec2(40, 77)))

    def create_player(self):
        self.__player__ = Player()
        instance_create(self.__player__)
        self.__camera__ = FightCameraObj(self.__player__, self.tileMap)

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.__phyManager__.update()
        self.__phyManager__.check('player', 'barrage')
        self.__phyManager__.check('pl_bullet', 'enemy')
        if self.__camera__ is not None:
            self.__camera__.update(game_args)

    def instance_create(self, obj: GameObject):
        super().instance_create(obj)
        if isinstance(obj, Collidable):
            self.__phyManager__.insert_object(obj)

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

