import importlib.util

from Core.GameStates import GameState
from Core.GameStates.GameState import *
from Core.GamingGL.GLShader import *
from Core.MathUtil import FRect
from Core.Profile.Savable import *
from Game.Characters.Humans.Player import PlayerData
from Game.Components.PauseUI import PauseUI
from Game.Map.Framework.TileMap import TileMap
from Game.Map.Framework.Tiles import TILE_LENGTH
from Game.Map.Framework.WorldData import WorldData, __wdTransfer__, __set_start_type__
from Core.Physics.Easings import *

import inspect

__difficulty__ = Savable[int]('global\\mode.diff.meta')
__diffDynamic__ = Savable[float]('global\\mode.diff.dyna')

__worldPlayerPosX__ = Savable[float]('global\\loc.ppos.x')
__worldPlayerPosY__ = Savable[float]('global\\loc.ppos.y')
__worldRoomX__ = Savable[int]('global\\loc.room.x')
__worldRoomY__ = Savable[int]('global\\loc.room.y')
__worldRespawnTime__ = Savable[int]('global\\stat.respawn')
__worldElapsedTime__ = Savable[float]('global\\stat.time.tot', 0.0)
__worldElapsedTimeVTOT__ = __worldElapsedTime__.value

from Game.Scenes.FightScene.SceneMain import FightScene
from Resources.ResourceLib import Sounds

if __worldRoomX__.value is None:
    __worldRoomX__.value = -1
if __worldRoomY__.value is None:
    __worldRoomY__.value = -1
if __worldPlayerPosX__.value is None:
    __worldPlayerPosX__.value = 72.0
if __worldPlayerPosY__.value is None:
    __worldPlayerPosY__.value = 192.0 + 48.0
if __worldRespawnTime__.value is None:
    __worldRespawnTime__.value = 0

if __difficulty__.value is None:
    __difficulty__.value = 2
if __diffDynamic__.value is None:
    __diffDynamic__.value = 0


__worldCurRoom__: TileMap


def __quitSave__():

    __worldElapsedTime__.value = __worldElapsedTimeVTOT__
    ProfileIO.save()


def __wmSave__(player_pos: vec2):

    __worldRoomX__.value = int(__worldCurRoom__.worldPos.x)
    __worldRoomY__.value = int(__worldCurRoom__.worldPos.y)
    __worldPlayerPosX__.value = player_pos.x
    __worldPlayerPosY__.value = player_pos.y
    __worldElapsedTime__.value = __worldElapsedTimeVTOT__
    ProfileIO.save()


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
    old_image: RenderTarget
    bottom: float

    def __init__(self):
        super().__init__()
        self.old_image = GameState.__gsSurfaceManager__.screen.copy_to(GameState.__gsSurfaceManager__.buffers[5])
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
            FRect(0, 0, surface_manager.__curSize__.x, self.bottom)
        )


class DefaultFightScene(FightScene):
    __tileMap__: TileMap
    __playerPos__: vec2
    __playerSpeedRemain__: vec2
    __bottom__: float
    __fade_in__: bool
    __timeElapsed__: float
    __died_progress__: float
    __main_alpha__: float
    timer: float
    __overlay_pos__: vec2
    __warnIntensity__: float
    __old_hp__: float
    __hit_blur__: float
    __pause_ui__: PauseUI
    __save_blur__: float
    __died_blur__: float
    __save_end_progress__: float

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
        self.__pause_ui__ = PauseUI(Action(self.resume_game))
        self.__save_blur__ = 0.0
        self.__old_hp__ = -1.0
        self.__main_alpha__ = 1.0
        self.__save_end_progress__ = 0.0
        self.__hit_blur__ = 0.0
        self.__warnIntensity__ = 0.0
        self.timer = 0.0
        self.__overlay_pos__ = vec2(0, 0)
        self.__bottom__ = 0.0
        self.__timeElapsed__ = 0.0
        self.__died_progress__ = 0.0
        self.__died_blur__ = 0.0
        self.__fade_in__ = fade_in
        if player_pos.y >= 0:
            self.__playerPos__ = player_pos
            self.__playerPos__.y = tile_map.height * TILE_LENGTH - self.__playerPos__.y
        else:
            self.__playerPos__ = player_pos
            self.__playerPos__.y *= -1
        self.__tileMap__ = tile_map
        self.player_data = data
        self.__playerSpeedRemain__ = speed_remain

    def start(self):
        if self.__fade_in__:
            instance_create(DelayedAction(0.7, Action(self.__recover_fade__)))
            self.__bottom__ = GameState.__gsRenderOptions__.screenSize.y
            EasingRunner(0.7, self.__bottom__, 0, EaseType.quint).run(self.__set_bottom__)
        self.set_tiles(self.__tileMap__)
        self.create_player(self.__playerPos__, self.__playerSpeedRemain__, self.player_data)
        teleport_pos = self.__playerPos__

        if teleport_pos.x <= 0:
            teleport_pos.x = self.__tileMap__.width * TILE_LENGTH + teleport_pos.x
            self.__player__.image.flip = True
        if teleport_pos.y <= 0:
            teleport_pos.y = self.__tileMap__.height * TILE_LENGTH + teleport_pos.y

        self.__player__.teleport(teleport_pos)
        self.instance_create(self.__pause_ui__)

        for obj in self.tileMap.get_objects():
            instance_create(obj)

    def __respawn_scene__(self):
        WorldManager.play_respawn_scene()

    def pause_game(self):
        super().pause_game()
        self.__pause_ui__.on_activate()
        Sounds.pause.play()

    def resume_game(self):
        super().resume_game()
        Sounds.pause.play()

    def update(self, game_args: GameArgs):
        global __worldElapsedTimeVTOT__
        __worldElapsedTimeVTOT__ += game_args.elapsedSec
        __wdTransfer__((__worldElapsedTimeVTOT__, __worldRespawnTime__))

        if key_on_press(KeyIdentity.pause) and self.tileMap.savable:
            if self.is_pause:
                self.resume_game()
            elif not self.__fade_in__:
                self.pause_game()
                rm = GameState.__gsSurfaceManager__
                rm.screen.copy_to(rm.buffers[7])

        self.__main_alpha__ = Math.lerp(
            self.__main_alpha__, 0.5 if self.is_pause else 1,
            min(1.0, 32 * game_args.elapsedSec)
        )

        super().update(game_args)
        self.__timeElapsed__ = game_args.elapsedSec
        self.timer += game_args.elapsedSec

        self.__save_end_progress__ = Math.lerp(self.__save_end_progress__, 0.0, min(1.0, game_args.elapsedSec * 1.2))

        if self.player is None or self.player.__dead__:
            self.__died_progress__ += game_args.elapsedSec * 1.5
            self.__died_progress__ = min(self.__died_progress__, 1.0)
            self.__died_blur__ = Math.lerp(self.__died_blur__, 2.3, game_args.elapsedSec * 3.0)

        if self.__player__ is None:
            return

        spg = self.__player__.save_progress()
        if spg > 1e-7:
            self.__save_blur__ = pow(spg, 0.35) * 4.0
        else:
            self.__save_blur__ = Math.lerp(self.__save_blur__, 0.0, min(1.0, game_args.elapsedSec * 20.0))

        if not self.__player__.__dead__:
            self.__overlay_pos__ = self.__camera__.centre - vec2(200, 0) + vec2(
                Math.sin(self.timer * 0.54) * 47,
                Math.sin(self.timer * 0.42 + 0.7) * 26 + 26
            )

        if self.__old_hp__ < 0:
            self.__old_hp__ = self.player.hp.__hp__

        if self.__old_hp__ != self.player.hp.__hp__:
            self.__old_hp__ = self.player.hp.__hp__
            self.__hit_blur__ = 2.5

        if self.__hit_blur__ > 0:
            self.__hit_blur__ = Math.lerp(self.__hit_blur__, 0.0, game_args.elapsedSec * 10.0)

        speed = vec2(self.player.__lastSpeedX__, self.player.__ySpeed__)
        map_h = self.tileMap.height * TILE_LENGTH
        if self.__player__.areaRect.x + 32 > self.tileMap.width * TILE_LENGTH:
            pos = self.tileMap.worldPos
            WorldManager.change_map(
                int(pos.x + 1), int(pos.y),
                vec2(24, map_h - self.player.centre.y), speed, False, self.player.data
            )
        elif self.player.areaRect.x < 0:
            pos = self.tileMap.worldPos
            if not WorldManager.exist_map(pos.x - 1, pos.y):
                return
            WorldManager.change_map(
                int(pos.x - 1), int(pos.y),
                vec2(-24, map_h - self.player.centre.y), speed, False, self.player.data
            )
        elif self.player.areaRect.y < -16:
            pos = self.tileMap.worldPos
            if not WorldManager.exist_map(pos.x, pos.y + 1):
                return
            WorldManager.change_map(
                int(pos.x), int(pos.y + 1),
                vec2(self.player.centre.x, 32), vec2(speed.x, speed.y / 1.7 - self.player.jump_speed / 1.7), False, self.player.data
            )
        elif self.player.areaRect.bottom > self.tileMap.height * TILE_LENGTH + 31:
            pos = self.tileMap.worldPos
            if not WorldManager.exist_map(pos.x, pos.y - 1):
                return
            WorldManager.change_map(
                int(pos.x), int(pos.y - 1),
                vec2(self.player.centre.x, -16), speed, False, self.player.data
            )
        if self.player is not None:
            self.__warnIntensity__ = Math.lerp(
                self.__warnIntensity__, 1 - min(1, self.player.hp.__hp__ / self.player.hp.hp_max),
                self.__timeElapsed__ * 10
            )

    def on_save(self):
        self.__save_end_progress__ = 1.0
        __wmSave__(vec2(self.player.centre.x, self.tileMap.height * TILE_LENGTH - self.player.centre.y))

    def apply_shader(self, surface_manager: SurfaceManager):
        src = surface_manager.screen
        dst = surface_manager.buffers[6]
        sz = surface_manager.__renderOptions__.screenSize
        player_screen_delta = - self.camera.centre + vec2(sz.x / 2, sz.y / 2 - 24)
        # do motion blur:
        if GameState.__gsRenderOptions__.motionBlurEnabled:
            GamingGL.default_transform()
            dst.set_target_self()

            EffectLib.motion_blur.apply()
            scale = Math.clamp(self.__timeElapsed__ * 77.7 + (1 if self.player.__dead__ else 0), 0.01, 1.0)
            EffectLib.motion_blur.set_arg('scale', scale)
            EffectLib.motion_blur.set_arg('sampler', src)
            EffectLib.motion_blur.set_arg('sampler_old', surface_manager.buffers[7])
            EffectLib.motion_blur.set_arg('screen_size', sz)

            glBegin(GL_QUADS)

            data = [vec4(0, 0, 0, 0), vec4(sz.x, 0, 1, 0),
                    vec4(sz.x, sz.y, 1, 1), vec4(0, sz.y, 0, 1)]
            for i in range(4):
                glVertex4f(data[i].x, data[i].y, data[i].z, data[i].w)
                glTexCoord2f(data[i].z, data[i].w)

            glEnd()

            EffectLib.motion_blur.reset()
            src, dst = dst, src

        src.copy_to(surface_manager.buffers[7])

        split_intensity = max(0.0, (1 - self.__died_progress__) ** 3) * 32 / 1000
        if self.__died_progress__ <= 0.0001:
            split_intensity = 0.0
        if self.__save_blur__ > 0:
            split_intensity = max(split_intensity, self.__save_blur__ / 50.0)

        if split_intensity > 0.0001:
            GamingGL.default_transform()
            dst.set_target_self()

            EffectLib.rgbSplit.apply()
            EffectLib.rgbSplit.set_arg('iSplit', split_intensity)
            EffectLib.rgbSplit.set_arg('screen_size', sz)
            EffectLib.rgbSplit.set_arg('sampler', src)

            glBegin(GL_QUADS)

            data = [vec4(0, 0, 0, 0), vec4(sz.x, 0, 1, 0),
                    vec4(sz.x, sz.y, 1, 1), vec4(0, sz.y, 0, 1)]
            for i in range(4):
                glVertex4f(data[i].x, data[i].y, data[i].z, data[i].w)
                glTexCoord2f(data[i].z, data[i].w)

            glEnd()

            EffectLib.rgbSplit.reset()
            src, dst = dst, src

        step_intensity = 0.0
        step_intensity = max(step_intensity, self.__hit_blur__)
        step_intensity = max(step_intensity, self.__died_blur__)
        step_intensity = max(step_intensity, self.__save_blur__)

        # when player died, play seismic effect

        if self.player is None or self.player.__dead__ or self.__save_end_progress__ > 1e-2:
            GamingGL.default_transform()
            dst.set_target_self()

            seismic_pos = self.player.centre
            radius = 750.0
            prog = max(self.__died_progress__, 1 - self.__save_end_progress__)
            if self.player is None or self.__player__.__dead__:
                seismic_pos = self.__died_position__
                radius = 470.0

            EffectLib.seismic.apply()
            EffectLib.seismic.set_arg('iProgress', pow(prog, 0.333))
            EffectLib.seismic.set_arg('iRadius', radius)
            EffectLib.seismic.set_arg('iIntensity', 6.0)
            EffectLib.seismic.set_arg('iCentre', seismic_pos + player_screen_delta)
            EffectLib.seismic.set_arg('screen_size', sz)
            EffectLib.seismic.set_arg('sampler', src)

            glBegin(GL_QUADS)

            data = [vec4(0, 0, 0, 0), vec4(sz.x, 0, 1, 0),
                    vec4(sz.x, sz.y, 1, 1), vec4(0, sz.y, 0, 1)]
            for i in range(4):
                glVertex4f(data[i].x, data[i].y, data[i].z, data[i].w)
                glTexCoord2f(data[i].z, data[i].w)

            glEnd()

            EffectLib.seismic.reset()
            src, dst = dst, src

        if step_intensity > 0.1:
            GamingGL.default_transform()
            dst.set_target_self()

            EffectLib.stepSample.apply()
            EffectLib.stepSample.set_arg('iIntensity', step_intensity)
            EffectLib.stepSample.set_arg('iLightPos', self.player.centre + player_screen_delta)
            EffectLib.stepSample.set_arg('screen_size', sz)
            EffectLib.stepSample.set_arg('sampler', src)

            glBegin(GL_QUADS)

            data = [vec4(0, 0, 0, 0), vec4(sz.x, 0, 1, 0),
                    vec4(sz.x, sz.y, 1, 1), vec4(0, sz.y, 0, 1)]
            for i in range(4):
                glVertex4f(data[i].x, data[i].y, data[i].z, data[i].w)
                glTexCoord2f(data[i].z, data[i].w)

            glEnd()

            EffectLib.stepSample.reset()
            src, dst = dst, src

        polar_intensity = 0.0
        if polar_intensity > 0.0001:
            GamingGL.default_transform()
            dst.set_target_self()

            EffectLib.polar.apply()
            EffectLib.polar.set_arg('iIntensity', polar_intensity)
            EffectLib.polar.set_arg('iCentre', sz / 2)
            EffectLib.polar.set_arg('screen_size', sz)
            EffectLib.polar.set_arg('sampler', src)

            glBegin(GL_QUADS)

            data = [vec4(0, 0, 0, 0), vec4(sz.x, 0, 1, 0),
                    vec4(sz.x, sz.y, 1, 1), vec4(0, sz.y, 0, 1)]
            for i in range(4):
                glVertex4f(data[i].x, data[i].y, data[i].z, data[i].w)
                glTexCoord2f(data[i].z, data[i].w)

            glEnd()

            EffectLib.polar.reset()
            src, dst = dst, src

        if self.tileMap.overlay_image is not None:
            GamingGL.default_transform()
            dst.set_target_self()

            EffectLib.overlay.apply()
            EffectLib.overlay.set_arg('iIntensity', self.tileMap.overlay_intensity)
            EffectLib.overlay.set_arg('sampler', src)
            EffectLib.overlay.set_arg('iWarn', sin(self.__warnIntensity__ * 1.57) * 0.4)
            EffectLib.overlay.set_arg('iTime', self.timer)
            EffectLib.overlay.set_arg('iCamPos', self.__overlay_pos__ + self.tileMap.overlay_pos)
            EffectLib.overlay.set_arg('sampler_overlay', self.tileMap.overlay_image)
            EffectLib.overlay.set_arg('screen_size', sz)

            glBegin(GL_QUADS)

            data = [vec4(0, 0, 0, 0), vec4(sz.x, 0, 1, 0),
                    vec4(sz.x, sz.y, 1, 1), vec4(0, sz.y, 0, 1)]
            for i in range(4):
                glVertex4f(data[i].x, data[i].y, data[i].z, data[i].w)
                glTexCoord2f(data[i].z, data[i].w)

            glEnd()

            EffectLib.overlay.reset()
            src, dst = dst, src

        glUseProgram(0)
        glBindTexture(GL_TEXTURE_2D, 0)

        self.ui_painter.blit(src, self.__bottom__)
        return src

    def default_draw(self, surface_manager: SurfaceManager):
        if not self.__fade_in__:
            super().draw(surface_manager)
        else:
            self.__get_surfaces__(surface_manager)
            size = self.__render_options__.screenSize
            rec = FRect(0, self.__bottom__, size.x, size.y - self.__bottom__)
            surface_manager.screen.blit(
                surface_manager.get_surface('bg'),
                vec2(0, self.__bottom__),
                area=rec,
            )
            surface_manager.screen.blit(
                surface_manager.get_surface('default'),
                vec2(0, 48 + rec.y),
                area=rec,
            )
            if surface_manager.exist_surface('barrage'):
                surface_manager.screen.blit(
                    surface_manager.get_surface('barrage'),
                    vec2(0, 48 + rec.y),
                    area=rec,
                )

    def draw(self, surface_manager: SurfaceManager):
        if self.is_pause:
            src = surface_manager.buffers[7]

        else:
            self.default_draw(surface_manager)
            src = self.apply_shader(surface_manager)

        if self.__main_alpha__ >= 0.999:
            src.copy_to(surface_manager.screen)
        else:
            if self.is_pause:
                surface_manager.screen.blit_data(
                    src, RenderData(vec2(0, 0), color=vec4(self.__main_alpha__, self.__main_alpha__, self.__main_alpha__, 1.0))
                )
                GameState.__gsRenderOptions__.transform.alpha = 1.0
            else:
                src.copy_to(surface_manager.screen)
                GameState.__gsRenderOptions__.transform.alpha = self.__main_alpha__

        if self.is_pause:
            args = RenderArgs()
            args.camera_delta = vec2(0, 0)
            args.target_surface = surface_manager.screen
            self.__pause_ui__.draw(args)


class WorldManager:

    __worldNeedInitialize__: bool = True

    @staticmethod
    def save(player_pos: vec2):
        __wmSave__(player_pos)

    @staticmethod
    def get_map(x: int, y: int) -> TileMap:
        return WorldData.get_map(x, y)

    @staticmethod
    def exist_map(x: int, y: int) -> bool:
        return WorldData.exist_map(int(x), int(y))

    @staticmethod
    def change_map(x: int, y: int, pos: vec2, speed_remain: vec2, fade_in: bool = False, data: PlayerData = PlayerData()):
        global __worldCurRoom__
        __worldCurRoom__ = WorldData.get_map(x, y)
        change_scene(DefaultFightScene(
            __worldCurRoom__,
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
        GameState.__gsRenderOptions__.transform.reset()

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
        ProfileIO.restore_old()
        __worldRespawnTime__.value += 1
        ProfileIO.save()

    @staticmethod
    def start(start_type: type):
        WorldManager.respawn()
        __set_start_type__(start_type)
