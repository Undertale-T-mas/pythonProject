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
from Game.Scenes.FightScene.UIPaint import *


class FightCameraObj(Entity):
    __player__: Entity
    __map__: TileMap
    __changed__: bool

    __cur_x__: float | None
    __x_min__: float
    __x_max__: float

    __cur_y__: float | None
    __y_min__: float
    __y_max__: float
    __old_p__: vec2
    __tim__: float

    def __init__(self, player: Entity, _map: TileMap):
        super().__init__()
        self.__player__ = player
        self.__map__ = _map
        self.__changed__ = True
        self.__tim__ = 0.21
        self.__old_p__ = vec2(-1, -1)
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
            tar = Math.clamp(self.__player__.centre.x, self.__x_min__ - 2.0, self.__x_max__ + 2.0)
            self.__cur_x__ = self.__cur_x__ * (1 - lerp_scale) + tar * lerp_scale
            self.__cur_x__ = Math.clamp(self.__cur_x__, self.__x_min__, self.__x_max__)
            return self.__cur_x__

    def calc_y(self, lerp_scale: float):
        screen_y = GameState.__gsRenderOptions__.screenSize.y
        map_h = self.__map__.height * TILE_LENGTH
        if map_h <= screen_y:
            return screen_y / 2 - 24
        else:
            screen_y -= 72
            if self.__cur_y__ is None:
                self.__cur_y__ = self.__player__.centre.y
            tar = Math.clamp(self.__player__.centre.y, self.__y_min__ - 2.0, self.__y_max__ + 2.0)
            self.__cur_y__ = self.__cur_y__ * (1 - lerp_scale) + tar * lerp_scale
            self.__cur_y__ = Math.clamp(self.__cur_y__, self.__y_min__, self.__y_max__)
            return self.__cur_y__

    def update(self, args: GameArgs):
        lerp_s = min(1.0, args.elapsedSec * 12.0)

        self.centre.x = self.calc_x(lerp_s)
        self.centre.y = self.calc_y(lerp_s)

        if (self.centre - self.__old_p__).length_squared() > 0.1:
            self.__old_p__ = self.centre.copy()
            self.__changed__ = True
        else:
            self.__changed__ = False

        if self.__tim__ > 0:
            self.__tim__ -= args.elapsedSec
            self.__changed__ = True

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

        intensity = 144.0
        ease = EasingRunner(0.04, vec2(0, 0), Math.vec2_polar(intensity, direction), EaseType.cubic)
        for i in range(8):
            intensity *= 0.76
            self.direction += Math.rand(166, 194)
            ease.to(0.045, Math.vec2_polar(intensity, self.direction), EaseType.cubic)
        ease.to(0.045, vec2(0, 0), EaseType.cubic)
        ease.run(self.set_camera)

    def update(self, args: GameArgs):
        pass


class FightScene(TileMapScene):
    __phyManager__: PhysicManager
    __player__: Player
    __a_camera__: FightCameraObj
    ui_painter: UIPainter
    __on_kill__: bool
    __died_position__: vec2

    @property
    def player(self):
        return self.__player__

    def __init__(self):
        super().__init__()
        self.ui_painter = UIPainter()
        self.__on_kill__ = False
        self.__phyManager__ = PhysicManager()

    def __move_player__(self):
        self.__player__.centre = vec2(-1000, -1000)

    def __respawn_scene__(self):
        raise Exception()

    def remove_player(self, shake_dir: float, died_pos: vec2):
        self.__died_position__ = died_pos
        y_max = GameState.__gsRenderOptions__.screenSize.y
        if self.__died_position__.y > y_max:
            self.__died_position__.y = y_max
        self.instance_create(Shaker(self.__camera__, shake_dir))
        self.__camera__.dispose()
        self.__player__.dispose()
        self.ui_painter.dead()
        self.__on_kill__ = True
        self.instance_create(DelayedAction(0, Action(self.__move_player__)))
        self.__player__.image.imageSource = self.player.__image_set__.imageDict['Punk_death']
        self.instance_create(DeathAnimation(self.__player__.image, self.__player__, vec2(20, 30), vec2(40, 77)))
        self.instance_create(DelayedAction(0.6, Action(self.__respawn_scene__)))

    def create_player(self, pos: vec2 = (24, 0), speed: vec2 = vec2(0, 0), data: PlayerData = PlayerData()):
        self.__player__ = Player(pos, speed, data)
        instance_create(self.__player__)
        wp = self.tileMap.__worldPos__
        if WorldData.exist_map(int(wp.x), int(wp.y - 1)):
            self.__player__.dropDead = False
        self.__a_camera__ = FightCameraObj(self.__player__, self.tileMap)
        self.__camera__ = self.__a_camera__

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.ui_painter.update(game_args)
        self.__phyManager__.update()
        self.__phyManager__.check('player', 'barrage')
        self.__phyManager__.check('pl_bullet', 'enemy')
        if self.__camera__ is not None:
            if self.__camera__.is_disposed():
                return
            self.__camera__.update(game_args)

    def on_save(self):
        raise NotImplementedError()

    def instance_create(self, obj: GameObject):
        super().instance_create(obj)
        if isinstance(obj, Collidable):
            self.__phyManager__.insert_object(obj)

    def draw(self, surface_manager: SurfaceManager):
        if self.__a_camera__ is not None:
            surface_manager.set_visible('bg', self.__a_camera__.__changed__ or self.__on_kill__ or self.tileChanged)

        super().draw(surface_manager)
        rec = FRect(0, 0, self.__render_options__.screenSize.x, self.__render_options__.screenSize.y - 0)
        surface_manager.screen.blit(
            surface_manager.get_surface('bg'),
            vec2(0, 0),
            area=rec,
        )
        rec = FRect(0, 0, self.__render_options__.screenSize.x, self.__render_options__.screenSize.y - 48)
        surface_manager.screen.blit(
            surface_manager.get_surface('default'),
            vec2(0, 48),
            area=rec,
        )
        rec = FRect(0, 0, self.__render_options__.screenSize.x, self.__render_options__.screenSize.y - 48)
        if surface_manager.exist_surface('barrage'):
            surface_manager.screen.blit(
                surface_manager.get_surface('barrage'),
                vec2(0, 48),
                area=rec,
            )
