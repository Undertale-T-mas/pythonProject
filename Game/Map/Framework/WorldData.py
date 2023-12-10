__map_array__: dict = dict()
__world_difficulty__: int = 0
__world_difficulty_adjust__: float = 0.0

from Core.GameObject import Entity


class WorldData:

    @staticmethod
    def insert(single_map: Entity, x: int, y: int):
        __map_array__[((x + 10) << 10) + y] = single_map
        pass

    @staticmethod
    def get_map(x: int, y: int):
        tar = __map_array__[((x + 10) << 10) + y]
        return type(tar)()

    @staticmethod
    def get_difficulty():
        return __world_difficulty__

    @staticmethod
    def get_difficulty_adjust():
        return __world_difficulty_adjust__
