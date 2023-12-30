from Game.Components.UIButton import *
import requests
import threading
import json


class ScoreUnit:
    username: str
    time_cost: float
    time_finished: str

    def __init__(self, username: str, time_cost: float, time_finished: str):
        self.username = username
        self.time_finished = time_finished
        self.time_cost = time_cost

    def draw_at(self, pos: vec2, surf: RenderTarget):
        t_t = self.time_cost
        ResourceLib.Fonts.pix0.blit(
            surf,
            str.format("{:0>2d}:{:0>2d}.{:.0f}", int(t_t / 60), int(t_t) % 60, int(10 * Math.fract(t_t))),
            pos, col=cv4.YELLOW, scale=0.6
        )


class ScoreBoard(Entity, IHandlerUI):

    buttonManager: ButtonManager

    _loading: bool
    _delta_tar: vec2
    activated: bool
    scores: List[ScoreUnit]
    _button_count: int
    fa: IHandlerUI

    def _request_url(self):
        url = "http://uf-ex.com:3333/rank/level-1"
        response = requests.get(url)
        content = response.content
        status_code = response.status_code

        print('sent a request to server:', url)
        print(f"status code: {status_code}")
        print(f"content: {content}")

        response_dict = json.loads(content)
        data = response_dict['data']
        for obj in data:
            self.scores.append(ScoreUnit(obj['username'], obj['time'], obj['update_time']))

        self._loading = False

    def load(self):
        self.scores = []
        self._loading = True
        thread = threading.Thread(self._request_url())
        thread.start()

    def on_activate(self):
        self.centre = vec2(700.0, 0.0)
        self.buttonManager.on_activate()
        self.load()
        self._delta_tar = vec2(0.0, 0.0)
        self.activated = True

    def on_deactivate(self):
        self.buttonManager.on_deactivate()
        self._delta_tar = vec2(700.0, 0.0)
        self.activated = False

    def back(self):
        self.fa.on_activate()
        self.on_deactivate()

    page: int

    def pgleft(self):
        self.page -= 1
        if self.page < 0:
            self.page = 0

    def pgright(self):
        pass

    def __init__(self, fa: IHandlerUI):
        self.scores = []
        self.fa = fa
        super().__init__()
        self.centre = vec2(700.0, 0.0)
        self.activated = False
        self.buttonManager = ButtonManager()
        self.page = 0
        self.buttonManager.appear_delta = vec2(700.0, 0.0)
        sz = GameState.__gsRenderOptions__.screenSize
        self.buttonManager.show_enable = False
        self.buttonManager.buttons.append(Button('<', vec2(sz.x / 2 - 155, 234), Action(self.pgleft)))
        self.buttonManager.buttons.append(Button('back', vec2(sz.x / 2, 234), Action(self.back)))
        self.buttonManager.buttons.append(Button('>', vec2(sz.x / 2 + 155, 234), Action(self.pgright)))
        self.buttonManager.focus_on(1)

        self._button_count = self.buttonManager.button_count

    def update(self, args: GameArgs):
        self.centre = self.buttonManager.delta

        if self.activated:
            self.buttonManager.update(args)

        if self.activated:
            if key_on_press(ki.right):
                cur = self.buttonManager.focus
                if cur < self._button_count - 1:
                    self.buttonManager.focus_on(cur + 1)
                    Sounds.uiSwitch.play()

            elif key_on_press(ki.left):
                cur = self.buttonManager.focus
                if cur != 0:
                    self.buttonManager.focus_on(cur - 1)
                    Sounds.uiSwitch.play()

    def draw(self, render_args: RenderArgs):
        self.buttonManager.draw(render_args)

        sz = GameState.__gsRenderOptions__.screenSize
        ResourceLib.Fonts.evil_empire.blit(
            render_args.target_surface, '>> Scoreboard <<', vec2(sz.x / 2, 144) + self.centre,
            col=vec4(1.0, 1.0, 1.0, 1.0)
        )

        if not self._loading:
            f = ResourceLib.Fonts.evil_empire
            pos = vec2(sz.x / 2, 300)
            for obj in self.scores:
                f.blit(render_args.target_surface, obj.username, pos - vec2(250, 0) + self.centre, vec2(0, 0), scale=0.5)
                t_t = obj.time_cost
                time_text = str.format("{:0>2d}:{:0>2d}.{:.0f}", int(t_t / 60), int(t_t) % 60, int(10 * Math.fract(t_t)))
                f.blit(render_args.target_surface, time_text, pos - vec2(50.0, 0) + self.centre, vec2(0, 0), col=cv4.YELLOW, scale=0.5)
                f.blit(render_args.target_surface, obj.time_finished, pos + vec2(120.0, 0) + self.centre, vec2(0, 0), scale=0.5)
                pos.y += 40
