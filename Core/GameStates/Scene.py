from Core.GameStates.ObjectManager import *
from Core.Render.SurfaceManager import *
from Core.GameStates import GameStates


class Scene:
    __objManager__ = ObjectManager()
    __render_args__ = RenderArgs()
    __render_options__: RenderOptions
    __initialized__ = False

    def start(self):
        pass

    def __init__(self):
        self.__render_options__ = GameStates.__gsRenderOptions__

    def update(self, game_args: GameArgs):
        if not self.__initialized__:
            self.__initialized__ = True
            self.start()
        self.__objManager__.update_all(game_args)

    def __get_surfaces__(self, manager: SurfaceManager):
        manager.draw_begin()
        for obj in self.__objManager__.get_objects():
            if isinstance(obj, Entity):
                manager.draw_insert(obj)

        manager.draw_end(self.__render_args__)

    def instance_create(self, obj: GameObject):
        self.__objManager__.instance_create(obj)

    def draw(self, surface_manager: SurfaceManager):
        self.__get_surfaces__(surface_manager)
