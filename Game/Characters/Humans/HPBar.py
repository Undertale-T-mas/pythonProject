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
        if not isinstance(GameState.__gsScene__, TileMapScene):
            raise Exception()
        self.__scene__ = GameState.__gsScene__
        self.__difficulty__ = self.__scene__.scene_difficulty
        self.__player__ = player
        self.recover()

    def recover(self):
        self.__hp__ = self.hp_max

    def take_damage(self, damage_level: int):
        defense_level = TechData.get_defense()
        val = Math.damage(damage_level, defense_level)

        self.__hp__ -= val
        if self.__hp__ < 0:
            self.__player__.died()
