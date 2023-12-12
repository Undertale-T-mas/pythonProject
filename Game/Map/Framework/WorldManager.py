import importlib.util

from Core.GameStates import GameState
from Core.GameStates.GameState import *
from Core.Profile.Savable import *
from Game.Characters.Humans.Player import PlayerData
from Game.Map.Framework.MapGenerate import AutoTileMap
from Game.Map.Framework.TileMap import TileMap
from Game.Map.Framework.Tiles import TILE_LENGTH
from Game.Map.Framework.WorldData import WorldData
from pygame import Vector2 as vec2
from Core.Physics.Easings import *

import inspect

__difficulty__ = Savable[int]('global\\mode.diff.meta')
__diffDynamic__ = Savable[float]('global\\mode.diff.dyna')

__worldPlayerPosX__ = Savable[float]('global\\loc.ppos.x')
__worldPlayerPosY__ = Savable[float]('global\\loc.ppos.y')
__worldRoomX__ = Savable[int]('global\\loc.room.x')
__worldRoomY__ = Savable[int]('global\\loc.room.y')
__worldRespawnTime__ = Savable[int]('global\\stat.respawn')

from Game.Scenes.FightScene import FightScene

if __worldRoomX__.value is None:
    __worldRoomX__.value = -1
if __worldRoomY__.value is None:
    __worldRoomY__.value = -1
if __worldPlayerPosX__.value is None:
    __worldPlayerPosX__.value = 24.0
if __worldPlayerPosY__.value is None:
    __worldPlayerPosY__.value = 48.0
if __worldRespawnTime__.value is None:
    __worldRespawnTime__.value = 0

if __difficulty__.value is None:
    __difficulty__.value = 0
if __diffDynamic__.value is None:
    __diffDynamic__.value = 0


__worldCurRoom__: TileMap


def get_all_subclasses(folder_path, base_class):
    derived_classes = []

    for entry in os.scandir(folder_path):
        if entry.is_file() and entry.name.endswith('.py'):
            module_name = entry.name[:-3]
            module_spec = importlib.util.spec_from_file_location(module_name, entry.path)
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)

            # 检查模块中的类
            for _name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, base_class) and obj != base_class and _name != 'AutoTileMap':
                    derived_classes.append(obj)

        elif entry.is_dir():
            subfolder_path = os.path.join(folder_path, entry.name)
            derived_classes.extend(get_all_subclasses(subfolder_path, base_class))

    return derived_classes


class RespawnScene(Scene):
    old_image: Surface
    bottom: float

    def __init__(self):
        super().__init__()
        self.old_image = GameState.__gsSurfaceManager__.screen.copy()
        self.bottom = GameState.__gsRenderOptions__.screenSize.y

    def set_bottom(self, val: float):
        self.bottom = val

    def __respawn__(self):
        WorldManager.respawn(True)

    def __ease_out__(self):
        EasingRunner(0.65, self.bottom, 0, EaseType.cubic).run(self.set_bottom)

    def start(self):
        instance_create(DelayedAction(0.05, Action(self.__ease_out__)))
        instance_create(DelayedAction(0.7, Action(self.__respawn__)))

    def update(self, game_args: GameArgs):
        super().update(game_args)

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager)
        surface_manager.screen.blit(
            self.old_image,
            vec2(0, 0),
            Rect(0, 0, surface_manager.__curSize__.x, self.bottom)
        )


class DefaultFightScene(FightScene):
    __tileMap__: TileMap
    __playerPos__: vec2
    __playerSpeedRemain__: vec2
    __bottom__: float
    __fade_in__: bool
    __playerData__: PlayerData

    def __recover_fade__(self):
        self.__fade_in__ = False

    def __set_bottom__(self, val: float):
        self.__bottom__ = val

    def __init__(self,
                 tile_map: TileMap,
                 player_pos: vec2,
                 speed_remain: vec2,
                 fade_in: bool = False,
                 data: PlayerData = PlayerData()
                 ):
        super().__init__()
        self.__fade_in__ = fade_in
        self.__playerPos__ = player_pos
        self.__tileMap__ = tile_map
        self.__playerData__ = data
        self.__playerSpeedRemain__ = speed_remain

    def start(self):
        if self.__fade_in__:
            instance_create(DelayedAction(0.7, Action(self.__recover_fade__)))
            self.__bottom__ = GameState.__gsRenderOptions__.screenSize.y
            EasingRunner(0.7, self.__bottom__, 0, EaseType.quint).run(self.__set_bottom__)
        self.set_tiles(self.__tileMap__)
        self.create_player(self.__playerPos__, self.__playerSpeedRemain__, self.__playerData__)
        teleport_pos = self.__playerPos__

        if teleport_pos.x <= 0:
            teleport_pos.x = self.__tileMap__.width * TILE_LENGTH + teleport_pos.x
        if teleport_pos.y <= 0:
            teleport_pos.y = self.__tileMap__.height * TILE_LENGTH + teleport_pos.y

        self.__player__.teleport(teleport_pos)

        for obj in self.tileMap.get_objects():
            instance_create(obj)

    def __respawn_scene__(self):
        WorldManager.play_respawn_scene()

    def update(self, game_args: GameArgs):
        super().update(game_args)
        if self.__player__ is None:
            return
        speed = vec2(self.player.__lastSpeedX__, self.player.__ySpeed__)
        if self.__player__.areaRect.x + 32 >= self.tileMap.width * TILE_LENGTH:
            pos = self.tileMap.worldPos
            WorldManager.change_map(
                int(pos.x + 1), int(pos.y),
                vec2(24, self.player.centre.y), speed, False, self.player.data
            )
        elif self.player.areaRect.x <= 0:
            pos = self.tileMap.worldPos
            WorldManager.change_map(
                int(pos.x - 1), int(pos.y),
                vec2(-24, self.player.centre.y), speed, False, self.player.data
            )

    def draw(self, surface_manager: SurfaceManager):
        if not self.__fade_in__:
            super().draw(surface_manager)
            return
        self.__get_surfaces__(surface_manager)
        size = self.__render_options__.screenSize
        rec = pygame.rect.Rect(0, self.__bottom__, size.x, size.y - self.__bottom__)
        surface_manager.screen.blit(
            surface_manager.get_surface('bg'),
            dest=rec,
            area=rec,
        )
        surface_manager.screen.blit(
            surface_manager.get_surface('default'),
            dest=vec2(0, 48 + rec.y),
            area=rec,
        )
        if surface_manager.exist_surface('barrage'):
            surface_manager.screen.blit(
                surface_manager.get_surface('barrage'),
                dest=vec2(0, 48 + rec.y),
                area=rec,
            )


class WorldManager:

    __worldNeedInitialize__: bool = True

    @staticmethod
    def save(player_pos: vec2):
        __worldRoomX__.value = int(__worldCurRoom__.worldPos.x)
        __worldRoomY__.value = int(__worldCurRoom__.worldPos.y)
        __worldPlayerPosX__.value = player_pos.x
        __worldPlayerPosY__.value = player_pos.y
        ProfileIO.save()

    @staticmethod
    def get_map(x: int, y: int) -> TileMap:
        return WorldData.get_map(x, y)

    @staticmethod
    def change_map(x: int, y: int, pos: vec2, speed_remain: vec2, fade_in: bool = False, data: PlayerData = PlayerData()):
        change_scene(DefaultFightScene(
            WorldData.get_map(x, y),
            pos,
            speed_remain,
            fade_in,
            data
        ))

    @staticmethod
    def play_respawn_scene():
        change_scene(RespawnScene())

    @staticmethod
    def respawn(fade_in: bool = False):
        if WorldManager.__worldNeedInitialize__:
            TileMap.in_initialize = True
            WorldManager.__worldNeedInitialize__ = False
            maps = get_all_subclasses('Game\\Map', TileMap)
            for map_unit in maps:
                map_obj = map_unit()
                print(map_unit)
                WorldData.insert(map_obj, int(map_obj.worldPos.x), int(map_obj.worldPos.y))
            TileMap.in_initialize = False

        WorldManager.change_map(
            __worldRoomX__.value, __worldRoomY__.value,
            vec2(__worldPlayerPosX__.value, __worldPlayerPosY__.value),
            vec2(0, 0),
            fade_in
        )
        __worldRespawnTime__.value += 1
        ProfileIO.save()
