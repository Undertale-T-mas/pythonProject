from Core.Animation.Animation import Animation
from Core.GameStates.Scene import *
from Core.GameStates import *
import Core.GameStates.GameState
from Core.GameStates.GameState import *
from Core.Physics.Easings import *
from Game.Characters.Humans.Player import Player, PlayerData
from Game.Characters.Movable import DeathAnimation
from Game.Map.Framework.TileMap import *
from Game.Scenes.TileMapScene import *


class FightCameraObj(Entity):
    __player__: Entity
    __map__: TileMap

    __cur_x__: float | None
    __x_min__: float
    __x_max__: float

    __cur_y__: float | None
    __y_min__: float
    __y_max__: float

    def __init__(self, player: Entity, _map: TileMap):
        super().__init__()
        self.__player__ = player
        self.__map__ = _map
        self.centre = GameState.__gsRenderOptions__.screenSize / 2
        self.__cur_x__ = None
        self.__x_min__ = self.centre.x
        self.__x_max__ = _map.width * TILE_LENGTH - self.__x_min__
        self.__cur_y__ = None
        self.__y_min__ = self.centre.y - 24
        self.__y_max__ = _map.height * TILE_LENGTH - self.__y_min__ + 24

    def calc_x(self, lerp_scale: float):
        screen_x = GameState.__gsRenderOptions__.screenSize.x
        map_w = self.__map__.width * TILE_LENGTH
        if map_w <= screen_x:
            return screen_x / 2
        else:
            if self.__cur_x__ is None:
                self.__cur_x__ = self.__player__.centre.x
            self.__cur_x__ = self.__cur_x__ * (1 - lerp_scale) + self.__player__.centre.x * lerp_scale
            self.__cur_x__ = min(max(self.__cur_x__, self.__x_min__), self.__x_max__)
            return self.__cur_x__

    def calc_y(self, lerp_scale: float):
        screen_y = GameState.__gsRenderOptions__.screenSize.y - 72
        map_h = self.__map__.height * TILE_LENGTH
        if map_h <= screen_y:
            return screen_y / 2
        else:
            if self.__cur_y__ is None:
                self.__cur_y__ = self.__player__.centre.y
            self.__cur_y__ = self.__cur_y__ * (1 - lerp_scale) + self.__player__.centre.y * lerp_scale
            self.__cur_y__ = min(max(self.__cur_y__, self.__y_min__), self.__y_max__)
            return self.__cur_y__

    def update(self, args: GameArgs):
        lerp_s = min(1.0, args.elapsedSec * 12.0)
        self.centre.x = self.calc_x(lerp_s)
        self.centre.y = self.calc_y(lerp_s)

    def draw(self, render_args: RenderArgs):
        pass


class Shaker(GameObject):
    direction: float
    camera: Entity
    fix_p: vec2

    def set_camera(self, pos):
        self.camera.centre = pos + self.fix_p

    def __init__(self, camera: Entity, direction: float):
        self.camera = camera
        self.fix_p = self.camera.centre
        self.direction = direction

        intensity = 24.0
        ease = EasingRunner(0.04, vec2(0, 0), Math.vec2_polar(intensity, direction), EaseType.cubic)
        for i in range(6):
            intensity *= 0.76
            self.direction += Math.rand(150, 210)
            ease.to(0.05, Math.vec2_polar(intensity, self.direction), EaseType.cubic)
        ease.to(0.05, vec2(0, 0), EaseType.cubic)
        ease.run(self.set_camera)

    def update(self, args: GameArgs):
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

    def __respawn_scene__(self):
        raise Exception()

    def remove_player(self, shake_dir: float):
        self.instance_create(Shaker(self.__camera__, shake_dir))
        self.__camera__.dispose()
        self.__player__.dispose()
        self.instance_create(DelayedAction(0, Action(self.__move_player__)))
        self.__player__.image.imageSource = self.player.__image_set__.imageDict['Punk_death']
        self.instance_create(DeathAnimation(self.__player__.image, self.__player__, vec2(20, 30), vec2(40, 77)))
        self.instance_create(DelayedAction(0.6, Action(self.__respawn_scene__)))

    def create_player(self, pos: vec2 = (24, 0), speed: vec2 = vec2(0, 0), data: PlayerData = PlayerData()):
        self.__player__ = Player(pos, speed, data)
        instance_create(self.__player__)
        self.__camera__ = FightCameraObj(self.__player__, self.tileMap)

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.__phyManager__.update()
        self.__phyManager__.check('player', 'barrage')
        self.__phyManager__.check('pl_bullet', 'enemy')
        if self.__camera__ is not None:
            if self.__camera__.is_disposed():
                return
            self.__camera__.update(game_args)

    def instance_create(self, obj: GameObject):
        super().instance_create(obj)
        if isinstance(obj, Collidable):
            self.__phyManager__.insert_object(obj)

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager)
        rec = pygame.rect.Rect(0, 0, self.__render_options__.screenSize.x, self.__render_options__.screenSize.y - 0)
        surface_manager.screen.blit(
            surface_manager.get_surface('bg'),
            dest=rec,
            area=rec,
        )
        rec = pygame.rect.Rect(0, 0, self.__render_options__.screenSize.x, self.__render_options__.screenSize.y - 48)
        surface_manager.screen.blit(
            surface_manager.get_surface('default'),
            dest=vec2(0, 48),
            area=rec,
        )
        rec = pygame.rect.Rect(0, 0, self.__render_options__.screenSize.x, self.__render_options__.screenSize.y - 48)
        if surface_manager.exist_surface('barrage'):
            surface_manager.screen.blit(
                surface_manager.get_surface('barrage'),
                dest=vec2(0, 48),
                area=rec,
            )

