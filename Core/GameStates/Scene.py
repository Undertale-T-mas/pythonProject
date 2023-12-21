from Core.GameStates.ObjectManager import *
from Core.GamingGL.GLBase import GamingGL
from Core.Render.RenderOptions import RenderOptions
from Core.Render.SurfaceManager import *
from Core.Render.SurfaceManager import SurfaceManager


class Scene:
    __objManager__: ObjectManager
    __render_args__ = RenderArgs()
    __render_options__: RenderOptions
    __initialized__: bool
    __camera__: Entity | None

    @property
    def camera(self):
        return self.__camera__

    def __set_camera__(self, obj: Entity):
        self.__camera__ = obj

    def start(self):
        pass

    def __init__(self):
        self.__objManager__ = ObjectManager()
        self.__camera__ = None
        self.__initialized__ = False

    def __gsDataSend__(self, render_options: RenderOptions):
        self.__render_options__ = render_options

    def update(self, game_args: GameArgs):
        if not self.__initialized__:
            self.__initialized__ = True
            self.start()
        self.__objManager__.update_all(game_args)

    def __get_surfaces__(self, manager: SurfaceManager):
        manager.draw_begin()
        for obj in self.__objManager__.get_objects():
            if isinstance(obj, Entity):
                if obj.visible:
                    manager.draw_insert(obj)

        if self.__camera__ is None:
            self.__render_args__.camera_delta = vec2(0, 0)
        else:
            self.__render_args__.camera_delta = self.__camera__.centre - manager.__renderOptions__.screenSize * 0.5

        manager.draw_end(self.__render_args__)

    def instance_create(self, obj: GameObject):
        self.__objManager__.instance_create(obj)

    def draw(self, surface_manager: SurfaceManager):
        GamingGL.default_transform(surface_manager.__renderOptions__.screenSize)
        self.__get_surfaces__(surface_manager)
