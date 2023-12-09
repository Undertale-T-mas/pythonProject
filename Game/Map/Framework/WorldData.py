__map_array__: dict = dict()

from Core.GameObject import Entity


class WorldData:

    @staticmethod
    def insert(single_map: Entity, x: int, y: int):
        __map_array__[x << 10 + y] = single_map
        pass

    @staticmethod
    def get_map(x: int, y: int):
        return __map_array__[x << 10 + y]
