import Game.Map.Begin.MP_n1_n1

from Game.Scenes.FightScene.SceneMain import FightScene
from Game.Characters.Enemys.Robots import *


class TestScene(FightScene):
    time_tot = 0

    def __init__(self):
        super().__init__()

    def start(self):
        self.set_tiles(Game.Map.Begin.MP_n1_n1.MapTEST0())
        self.create_player()
        for obj in self.tileMap.get_objects():
            instance_create(obj)

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.time_tot += game_args.elapsedSec
        if self.time_tot > 1:
            self.time_tot -= 1

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager)

