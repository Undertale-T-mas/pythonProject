from core import *


__pdInstance__: Any


class IPlayer:

    def recharge_time(self):
        raise NotImplementedError()

    def died(self):
        raise NotImplementedError()

    def restore(self):
        raise NotImplementedError()


class PlayerData:
    def __init__(self, ammunition: int = 7, fire_cooldown: float = 0.0, hp: float = 999.0, difficulty: int = 0, obj: IPlayer = None):
        global __pdInstance__
        self.ammunition = ammunition
        self.fire_cooldown = fire_cooldown
        self.hp = hp
        self.difficulty = difficulty
        self.position = -vec2(10000, 10000)
        self.player_object = obj
        __pdInstance__ = self

    ammunition: int
    fire_cooldown: float
    hp: float
    difficulty: int
    position: vec2
    player_object: IPlayer

    def update_data(self, ammunition: int, fire_cooldown: float, hp: float, position: vec2, difficulty: int, obj: IPlayer):
        self.ammunition = ammunition
        self.fire_cooldown = fire_cooldown
        self.hp = hp
        self.player_object = obj
        self.position = position
        self.difficulty = difficulty


def get_player_data() -> PlayerData:
    return __pdInstance__
