from Resources.Music import *
from Core.GameStates.Scene import *
from Core.Profile.ProfileIO import *
from Core.Profile.Savable import Savable
from Game.Characters.Humans.Data import PlayerData
from Game.Map.Framework.TileMap import *


class TileMapScene(Scene):
    player_data: PlayerData
    tileMap: TileMap
    __difficulty__: int
    __diffDynamic__: float
    tileChanged: bool

    @property
    def savable(self):
        return self.tileMap.savable

    @property
    def player_controllable(self):
        return self.tileMap.player_controllable

    def on_save(self):
        raise NotImplementedError()

    def __init__(self):
        super().__init__()
        self.tileChanged = False
        self.__pause__ = False

    def set_tiles(self, tile_map: TileMap):
        self.tileMap = tile_map
        self.__difficulty__ = WorldData.get_difficulty()
        self.__diffDynamic__ = WorldData.get_difficulty_adjust()
        if tile_map.bgm != '':
            if tile_map.bgm == 'STOP':
                stop_music(1.0)
            else:
                play_music(tile_map.bgm, 1.0, 1.0)

        self.instance_create(self.tileMap)

    def update(self, game_args: GameArgs):
        self.tileChanged = False
        super().update(game_args)
        if self.tileMap.tileChanged:
            self.tileChanged = True

    @property
    def scene_difficulty(self):
        return self.__difficulty__

    __pause__: bool

    def pause_game(self):
        self.__focus_id__ = 1
        self.__pause__ = True

    def resume_game(self):
        self.__focus_id__ = 0
        self.__pause__ = False

    @property
    def is_pause(self):
        return self.__pause__

