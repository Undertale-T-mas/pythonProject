from Core.GameStates.ObjectManager import *
from Core.Render.SurfaceManager import *


class Scene:
    __objManager__ = ObjectManager()

    def update(self, game_args: GameArgs):
        self.__objManager__.update_all(game_args)

    def __get_surfaces__(self, manager: SurfaceManager):
        manager.draw_begin()
        for obj in self.__objManager__.get_objects():
            if isinstance(obj, Entity):
                manager.draw_insert(obj)
        manager.draw_end()

    def instance_create(self, obj: GameObject):
        self.__objManager__.instance_create(obj)

    def draw(self, surface_manager: SurfaceManager):
        self.__get_surfaces__(surface_manager)
