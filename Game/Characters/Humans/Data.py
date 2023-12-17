from core import *


__pdInstance__: Any


class PlayerData:
    def __init__(self, ammunition: int = 7, fire_cooldown: float = 0.0, hp: float = 999.0):
        global __pdInstance__
        self.ammunition = ammunition
        self.fire_cooldown = fire_cooldown
        self.hp = hp
        self.position = -vec2(10000, 10000)
        __pdInstance__ = self

    ammunition: int
    fire_cooldown: float
    hp: float
    position: vec2

    def update_data(self, ammunition: int, fire_cooldown: float, hp: float, position: vec2):
        self.ammunition = ammunition
        self.fire_cooldown = fire_cooldown
        self.hp = hp
        self.position = position


def get_player_data() -> PlayerData:
    return __pdInstance__
