import Game.Map.Begin.TestMap
import Resources.ResourceLib
from Resources.ResourceLib import *
from Core.MathUtil import *
import random
from Core.Physics.Easings import *

import pygame.draw_py
from pygame import *
import pygame
from Game.Characters.Humans.Player import *
from Core.GameStates.KeyIdentity import KeyIdentity as ki
from Game.Map.Framework.WorldManager import *


class Start(Scene):
    time_tot = 0

    text_1: Surface
    text_2: Surface
    text_start: Surface

    text_1_pos: vec2
    text_start_pos: vec2

    time_tot: float

    back_scale: List[float] = [0.0, 0.005, 0.015, 0.035, 0.067]
    back_images: List[Surface]

    def set_pos_1(self, pos: vec2):
        self.text_1_pos = pos

    def start(self):
        self.time_tot = 0
        self.text_1 = Fonts.kwark.render('Machine', False, [255, 222, 255, 255], [0, 0, 0, 0]) # .convert_alpha()
        self.text_2 = Fonts.kwark.render('Rebel', False, [255, 222, 255, 255], [0, 0, 0, 0]) # .convert_alpha()
        self.text_1 = self.text_1.convert_alpha()
        self.text_2 = self.text_2.convert_alpha()
        self.text_1.set_colorkey([0, 0, 0])
        self.text_2.set_colorkey([0, 0, 0])

        self.text_start = Fonts.evil_empire.render(
            '> press z or enter to start <', False,
            [255, 222, 255, 255],
            [0, 0, 0, 0]
        )

        self.text_1_pos = vec2(-650, 88)
        w, h = self.text_start.get_size()
        self.text_start = pygame.transform.scale(self.text_start, vec2(w, h) * 0.666)
        self.text_start_pos = vec2((GameState.__gsRenderOptions__.screenSize.x - self.text_start.get_width()) / 2, 500)
        self.text_start = self.text_start.convert_alpha()
        self.text_start.set_colorkey([0, 0, 0])
        EasingRunner(1.1, self.text_1_pos, vec2(185, 88), EaseType.back).run(self.set_pos_1)

        def set_alpha(v: float):
            for _i in range(len(self.back_images)):
                self.back_images[_i].set_alpha(int(v * 255))

        def alpha_ease():
            EasingRunner(0.7, 0.0,1.0, EaseType.quad).run(set_alpha)

        def set_alpha_max():
            set_alpha(1.0)
            if GameState.__gsRenderArgs__.quality <= 2:
                self.very_high_quality = False

        instance_create(DelayedAction(1.1, Action(alpha_ease)))
        instance_create(DelayedAction(1.8, Action(set_alpha_max)))

        self.back_images = []
        tar_y = GameState.__gsRenderOptions__.screenSize.y
        for i in range(len(self.back_scale)):
            self.back_images.append(load_image('BackGrounds\\Start\\' + str(i + 1) + '.png'))
            w, h = self.back_images[i].get_size()
            if h != tar_y:
                s = tar_y / h
                self.back_images[i] = pygame.transform.scale(
                    self.back_images[i],
                    vec2(w * s, h * s)
                )

        set_alpha(0)
        self.centre_x = 0.0
        self.very_high_quality = True
        pass

    centre_x: float
    very_high_quality: bool

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.time_tot += game_args.elapsedSec
        self.centre_x = Math.sin_deg(self.time_tot * 25.0) * 428.0

        if GameState.key_on_press(ki.confirm):
            WorldManager.respawn()

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager)

        surface_manager.buffers[0].fill([0, 0, 0, 0])

        if self.very_high_quality:
            surface_manager.buffers[1].fill([0, 0, 0, 0])
            for i in range(len(self.back_images)):
                surface_manager.buffers[1].blit(
                    self.back_images[i], vec2(self.centre_x * self.back_scale[i] * 0.6, 0)
                )

        surface_manager.buffers[0].blit(self.text_1, self.text_1_pos + vec2(self.centre_x * 0.05, 0))
        surface_manager.buffers[0].blit(self.text_2, self.text_1_pos + vec2(322 + self.centre_x * 0.05, 90))
        if self.time_tot >= 1.6:
            if self.time_tot % 0.8 < 0.42:
                surface_manager.buffers[0].blit(self.text_start, self.text_start_pos)

        surface_manager.screen.blit(surface_manager.buffers[1], vec2(0, 0))
        surface_manager.screen.blit(surface_manager.buffers[0], vec2(0, 0))
