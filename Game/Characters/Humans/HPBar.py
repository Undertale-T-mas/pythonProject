from Core.GameObject import GameObject
from Game.Characters.Movable import MovableEntity
from Game.Scenes.TileMapScene import *

from Game.Tech.DataLib import TechData

__playerHpChart__ = [30, 20, 20, 1]


class HPBar(GameObject):
    __scene__: TileMapScene
    __hp__: float
    __player__: MovableEntity
    __difficulty__: int

    @property
    def hp_max(self):
        return __playerHpChart__[self.__scene__.scene_difficulty]

    def __init__(self, player: MovableEntity):
        super().__init__()
        if not isinstance(GameState.__gsScene__, TileMapScene):
            raise Exception()
        self.__scene__ = GameState.__gsScene__
        self.__difficulty__ = self.__scene__.scene_difficulty
        self.__player__ = player
        self.recover()

    def recover(self):
        self.__hp__ = self.hp_max

    def get_nerf_scale(self):
        if self.__difficulty__ >= 2 and self.__scene__.tileMap.worldPos != vec2(2, 1):
            return 1
        return self.__scene__.tileMap.damage_nerf

    def take_damage(self, damage_level: int):
        defense_level = TechData.get_defense()
        val = Math.damage(damage_level, defense_level)

        self.__hp__ -= val * self.get_nerf_scale()
        if self.__hp__ < 0:
            self.__player__.died()
