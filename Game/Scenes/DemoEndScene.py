import threading

import requests

import Game.Map.Begin.MP_n1_n1
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


class DemoEndScene(Scene):
    time_tot = 0

    text_1: Texture
    text_2: Texture
    text_start: Texture

    text_1_pos: vec2
    text_start_pos: vec2
    back_alpha: float
    username: str
    start_tot: float

    death_text: str
    time_text: str
    char_last: str

    shader_time: float
    time_tot: float

    scoreboard_state: int

    tip_text: str
    time_value: float
    tip_color: vec4

    back_scale: List[float] = [0.0, 0.005, 0.015, 0.035, 0.067]
    back_images: List[Texture]

    _loading: bool

    def _request_url(self):

        try:

            url = f"http://uf-ex.com:3333/rank/level-1?username={self.username}&time={self.time_value}"
            response = requests.post(url)
            content = response.content
            status_code = response.status_code

            response_dict = json.loads(content)
            if response_dict['message'] != 'success':
                raise ConnectionError()

            print('sent a post to server:', url)
            print(f"status code: {status_code}")
            print(f"content: {content}")

            self.scoreboard_state = 1

        except e:

            self.scoreboard_state = -1
            print('failed connection')

        self._loading = False

    def name_invalid(self):
        if len(self.username) == 0:
            return True

        invalid_set = set()
        invalid_set.add(' ')
        invalid_set.add('/')
        invalid_set.add('=')
        invalid_set.add(',')
        invalid_set.add('?')

        for i in range(len(self.username)):
            if self.username[i] in invalid_set:
                return True

        return False

    def post(self):
        if self.scoreboard_state == -3 or self.scoreboard_state == 1:
            return

        if self.name_invalid():
            self.scoreboard_state = -2
            return

        self.scoreboard_state = -3
        self._loading = True
        try:
            thread = threading.Thread(self._request_url())
            thread.start()
        except e:
            self._loading = False
            self.scoreboard_state = -1
            print('Error in posting!')

    def set_pos_1(self, pos: vec2):
        self.text_1_pos = pos

    def make_tip(self):
        if self.scoreboard_state == -3:
            self.tip_text = 'please wait...'
            self.tip_color = cv4.YELLOW
        if self.scoreboard_state == -2:
            self.tip_text = 'invalid name!'
            self.tip_color = cv4.RED
        elif self.scoreboard_state == -1:
            self.tip_text = 'check connection!'
            self.tip_color = cv4.RED
        elif self.scoreboard_state == 0:
            self.tip_text = 'ENTER key > submit'
            self.tip_color = cv4.WHITE
        elif self.scoreboard_state == 1:
            self.tip_text = 'successful!'
            self.tip_color = cv4.LIME

    def start(self):
        self.back_alpha = 0.0
        self.scoreboard_state = 0
        self.time_tot = -0.000001
        self._loading = False
        self.char_last = ''
        self.shader_time = 0.0
        self.username = ''
        pygame.key.start_text_input()

        def p():
            play_music('Darkness Beyond.mp3', 1.0, 0.5)

        self.instance_create(DelayedAction(1.6, Action(p)))

        text_1 = Fonts.kwark.base_font.render('Machine', False, [255, 222, 255, 255], [0, 0, 0, 0]) # .convert_alpha()
        text_2 = Fonts.kwark.base_font.render('Rebel', False, [255, 222, 255, 255], [0, 0, 0, 0]) # .convert_alpha()
        text_1 = text_1.convert_alpha()
        text_2 = text_2.convert_alpha()
        text_1.set_colorkey([0, 0, 0])
        text_2.set_colorkey([0, 0, 0])

        self.start_tot = 0.0
        self.text_1_pos = vec2(-650, 88)

        self.death_text = str.format("Death {:0>5d}", int(WorldData.get_death_tot()))
        t_t = WorldData.get_time_tot()
        self.time_value = t_t
        self.time_text = str.format("Time {:0>2d}:{:0>2d}.{:.0f}", int(t_t / 60), int(t_t) % 60, int(10 * Math.fract(t_t)))

        text_start = Fonts.evil_empire.base_font.render(
            '> Demo ended. Thanks for playing <', False,
            [255, 222, 255, 255],
            [0, 0, 0, 0]
        )

        w, h = text_start.get_size()
        text_start = pygame.transform.scale(text_start, vec2(w, h) * 0.666)
        self.text_start_pos = vec2((GameState.__gsRenderOptions__.screenSize.x - text_start.get_width()) / 2, 500)
        text_start = text_start.convert_alpha()
        text_start.set_colorkey([0, 0, 0])
        EasingRunner(1.1, self.text_1_pos, vec2(185, 68), EaseType.back).run(self.set_pos_1)

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
        self.text_1 = Texture(text_1)
        self.text_2 = Texture(text_2)
        self.text_start = Texture(text_start)
        GameState.__gsRenderOptions__.transform.reset()
        pass

    centre_x: float
    very_high_quality: bool
    start_cooldown: float
    __timeElapsed__: float

    grid_sz = 0.39

    def update(self, game_args: GameArgs):
        super().update(game_args)
        self.__timeElapsed__ = game_args.elapsedSec
        self.time_tot += game_args.elapsedSec

        self.centre_x = Math.sin_deg(self.time_tot * 55.0) * 428.0

        self.shader_time += self.__timeElapsed__ * (1 - self.start_tot)

        k = key_input()
        if len(k) == 1 and len(self.username) < 12:
            if k == self.char_last:
                return
            self.char_last = k
            self.username += self.char_last
        else:
            self.char_last = ''

        if key_on_press(ki.delete):
            if len(self.username) >= 1:
                self.username = self.username[0:(len(self.username) - 1)]

        if key_on_press(ki.enter):
            self.post()

        self.make_tip()

    def draw(self, surface_manager: SurfaceManager):
        super().draw(surface_manager)

        surface_manager.screen.clear(cv4.TRANSPARENT)

        if self.very_high_quality:
            surface_manager.buffers[1].clear(cv4.TRANSPARENT)
            for i in range(len(self.back_images)):
                surface_manager.buffers[1].blit_data(
                    self.back_images[i],
                    RenderData(vec2(self.centre_x * self.back_scale[i] * 1.0 - 40, 0), color=cv4.WHITE * self.back_alpha)
                )

        src = surface_manager.buffers[1]
        dst = surface_manager.buffers[6]
        dst.clear(cv4.TRANSPARENT)
        sz = surface_manager.__renderOptions__.screenSize
        # do motion blur:
        if GameState.__gsRenderOptions__.motionBlurEnabled:
            GamingGL.default_transform()
            dst.set_target_self()

            EffectLib.grid.apply()
            EffectLib.grid.set_arg('sampler', src)
            EffectLib.grid.set_arg('iTime', self.shader_time + 0.000001)
            EffectLib.grid.set_arg(
                'iBlendColor',
                Math.lerp(
                    Math.lerp(Vector3(0.66, 0.63, 0.9), Vector3(0.89, 0.35, 0.87), sin(self.time_tot) * 0.5 + 0.5),
                    Vector3(1, 1, 1),
                    self.start_tot
                )
            )
            EffectLib.grid.set_arg('iDotSize', 0.39)
            EffectLib.grid.set_arg('screen_size', sz)

            glBegin(GL_QUADS)

            data = [vec4(0, 0, 0, 0), vec4(sz.x, 0, 1, 0),
                    vec4(sz.x, sz.y, 1, 1), vec4(0, sz.y, 0, 1)]
            for i in range(4):
                glVertex4f(data[i].x, data[i].y, data[i].z, data[i].w)
                glTexCoord2f(data[i].z, data[i].w)

            glEnd()

            EffectLib.grid.reset()
            src, dst = dst, src

        src.copy_to(surface_manager.screen)

        surface_manager.screen.blit(self.text_1, self.text_1_pos + vec2(self.centre_x * 0.05, 0))
        surface_manager.screen.blit(self.text_2, self.text_1_pos + vec2(322 + self.centre_x * 0.05, 90))
        if self.time_tot >= 1.6:
            if self.time_tot % 0.8 < 0.42:
                surface_manager.screen.blit(self.text_start, self.text_start_pos)

        screen = surface_manager.screen
        pf = Fonts.pix0
        pf.blit(screen, 'Game statistic:', vec2(100, 300), vec2(0, 0), cv4.WHITE * self.back_alpha, 0.75)
        pf.blit(screen, self.death_text, vec2(150, 345), vec2(0, 0), cv4.RED * self.back_alpha, 0.75)
        pf.blit(screen, self.time_text, vec2(150, 390), vec2(0, 0), cv4.YELLOW * self.back_alpha, 0.75)

        pf.blit(screen, 'Submit Scoreboard:', vec2(540, 300), vec2(0, 0), cv4.WHITE * self.back_alpha, 0.75)
        pf.blit(screen, 'name: ' + self.username, vec2(590, 345), vec2(0, 0), cv4.WHITE * self.back_alpha, 0.75)
        pf.blit(screen, self.tip_text, vec2(590, 390), vec2(0, 0), self.tip_color * self.back_alpha, 0.75)


