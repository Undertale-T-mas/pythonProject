from Game.Components.Score import ScoreBoard
from Game.Components.UIButton import *
from Game.Map.Framework.WorldData import WorldData
from Resources.ResourceLib import Sounds
from core import *


class PauseUI(Entity, IHandlerUI):

    buttonManager: ButtonManager
    _button_count: int
    _on_resume: Action
    _target: vec2
    _alpha: float
    handler_side: (Entity, IHandlerUI)
    scoreboard: ScoreBoard

    def resume(self):
        self._on_resume.act()

    def on_activate(self):
        self.reset_handler()
        Sounds.pause.play()
        self.centre = vec2(-600.0, 0.0)
        self._alpha = 0.0

    def quit(self):
        stop_game()

    def back(self):
        WorldData.back_to_menu()

    def reset_handler(self):
        self.set_handler(self.buttonManager)

    def score_enable(self):
        self.set_handler(self.scoreboard)

    def set_handler(self, obj: (Entity, IHandlerUI)):
        if self.handler_side is not None:
            self.handler_side.on_deactivate()

        self.handler_side = obj
        self.handler_side.on_activate()

    def __init__(self, on_resume: Action):
        super().__init__()
        self.handler_side = None
        self.scoreboard = ScoreBoard(self)
        self._target = vec2(0.0, 0.0)
        self._focus_id = 1
        self._alpha = 0.0
        self._on_resume = on_resume
        self.surfaceName = 'pause'
        self.buttonManager = ButtonManager()
        sz = GameState.__gsRenderOptions__.screenSize
        self.buttonManager.buttons.append(Button('resume', vec2(sz.x / 2, 300), Action(self.resume)))
        self.buttonManager.buttons.append(Button('back', vec2(sz.x / 2, 360), Action(self.back)))
        self.buttonManager.buttons.append(Button('quit', vec2(sz.x / 2, 420), Action(self.quit)))
        self.buttonManager.buttons.append(Button('score', vec2(sz.x / 2, 480), Action(self.score_enable)))
        self.buttonManager.focus_on(0)
        self.buttonManager.appear_delta = vec2(-600.0, 0.0)
        self._button_count = self.buttonManager.button_count
        self.reset_handler()

    def update(self, args: GameArgs):
        self.handler_side.update(args)
        if self.buttonManager != self.handler_side:
            self.buttonManager.update(args)

        if self.handler_side == self.buttonManager:
            if key_on_press(ki.down):
                cur = self.buttonManager.focus
                if cur < self._button_count - 1:
                    self.buttonManager.focus_on(cur + 1)
                    Sounds.uiSwitch.play()

            elif key_on_press(ki.up):
                cur = self.buttonManager.focus
                if cur != 0:
                    self.buttonManager.focus_on(cur - 1)
                    Sounds.uiSwitch.play()

        self.centre = self.buttonManager.delta
        self._alpha = Math.lerp(
            self._alpha,
            1.0 if self.handler_side == self.buttonManager else 0.5,
            args.elapsedSec * 20.0
        )

    def draw(self, render_args: RenderArgs):
        self.buttonManager.draw(render_args)
        if self.buttonManager != self.handler_side:
            self.handler_side.draw(render_args)

        sz = GameState.__gsRenderOptions__.screenSize
        ResourceLib.Fonts.evil_empire.blit(
            render_args.target_surface, '>> Game Paused <<', vec2(sz.x / 2, 144) + self.centre,
            col=vec4(1.0, 1.0, 1.0, self._alpha)
        )
