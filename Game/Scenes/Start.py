import Game.Map.Begin.TestMap
import Resources.ResourceLib
from Resources import ResourceLib
from Resources.ResourceLib import *
import random
from Resources.Music import *

import pygame.draw_py
from Game.Characters.Humans.Player import *
from Game.Map.Framework.WorldManager import *
from core import *
import core


class Start(Scene):
    time_tot = 0

    text_1: Texture
    text_2: Texture
    text_start: Texture

    text_1_pos: vec2
    text_start_pos: vec2
    back_alpha: float

    time_tot: float

    back_scale: List[float] = [0.0, 0.005, 0.015, 0.035, 0.067]
    back_images: List[Texture]

    def set_pos_1(self, pos: vec2):
        self.text_1_pos = pos

    def start(self):
        self.back_alpha = 0.0
        self.time_tot = 0

        def p():
            play_music('Darkness Beyond.mp3', 1.0, 0.5)

        self.instance_create(DelayedAction(1.6, Action(p)))

        text_1 = Fonts.kwark.base_font.render('Machine', False, [255, 222, 255, 255], [0, 0, 0, 0]) # .convert_alpha()
        text_2 = Fonts.kwark.base_font.render('Rebel', False, [255, 222, 255, 255], [0, 0, 0, 0]) # .convert_alpha()
        text_1 = text_1.convert_alpha()
        text_2 = text_2.convert_alpha()
        text_1.set_colorkey([0, 0, 0])
        text_2.set_colorkey([0, 0, 0])

        self.text_1_pos = vec2(-650, 88)

        text_start = Fonts.evil_empire.base_font.render(
            '> press z or enter to start <', False,
            [255, 222, 255, 255],
            [0, 0, 0, 0]
        )

        w, h = text_start.get_size()
        text_start = pygame.transform.scale(text_start, vec2(w, h) * 0.666)
        self.text_start_pos = vec2((GameState.__gsRenderOptions__.screenSize.x - text_start.get_width()) / 2, 500)
        text_start = text_start.convert_alpha()
        text_start.set_colorkey([0, 0, 0])
        EasingRunner(1.1, self.text_1_pos, vec2(185, 88), EaseType.back).run(self.set_pos_1)

        def set_alpha(v: float):
            self.back_alpha = v

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
            sur_tmp = load_image('BackGrounds\\Start\\' + str(i + 1) + '.png')
            w, h = sur_tmp.get_size()
            if h != tar_y:
                s = tar_y / h
                self.back_images.append(Texture(pygame.transform.scale(
                    sur_tmp,
                    vec2(w * s * 1.1, h * s)
                )))
            else:
                self.back_images.append(Texture(sur_tmp))

        set_alpha(0)
        self.centre_x = 0.0
        self.very_high_quality = True
        self.on_start = False
        self.text_1 = Texture(text_1)
        self.text_2 = Texture(text_2)
        self.text_start = Texture(text_start)
        pass

    centre_x: float
    very_high_quality: bool
    on_start: bool
    start_cooldown: float

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.time_tot += game_args.elapsedSec
        self.centre_x = Math.sin_deg(self.time_tot * 25.0) * 428.0

        if GameState.key_on_press(ki.confirm) and self.time_tot >= 1.6 and not self.on_start:
            self.on_start = True
            self.start_cooldown = 1.0
            Sounds.startGame.set_volume(0.5)
            Sounds.startGame.play()
            stop_music(0.4)

        if self.on_start:
            self.start_cooldown -= game_args.elapsedSec
            if self.start_cooldown <= -0.35:
                WorldManager.respawn()

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager)

        surface_manager.buffers[0].clear(cv4.TRANSPARENT)

        if self.very_high_quality:
            surface_manager.buffers[1].clear(cv4.TRANSPARENT)
            for i in range(len(self.back_images)):
                surface_manager.buffers[1].blit_data(
                    self.back_images[i],
                    RenderData(vec2(self.centre_x * self.back_scale[i] * 1.0 - 40, 0), color=cv4.WHITE * self.back_alpha)
                )

        surface_manager.buffers[0].blit(self.text_1, self.text_1_pos + vec2(self.centre_x * 0.05, 0))
        surface_manager.buffers[0].blit(self.text_2, self.text_1_pos + vec2(322 + self.centre_x * 0.05, 90))
        if self.time_tot >= 1.6:
            if self.on_start:
                if self.start_cooldown < 0 or self.start_cooldown % 0.2 > 0.11:
                    surface_manager.buffers[0].blit(self.text_start, self.text_start_pos)
            elif self.time_tot % 0.8 < 0.42:
                surface_manager.buffers[0].blit(self.text_start, self.text_start_pos)

        surface_manager.screen.blit(surface_manager.buffers[1], vec2(0, 0))
        surface_manager.screen.blit(surface_manager.buffers[0], vec2(0, 0))


