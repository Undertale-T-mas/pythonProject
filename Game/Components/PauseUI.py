from Game.Components.UIButton import *
from core import *


class PauseUI(Entity):

    buttonManager: ButtonManager
    _button_count: int
    _on_resume: Action

    def resume(self):
        self._on_resume.act()

    def quit(self):
        stop_game()

    def __init__(self, on_resume: Action):
        super().__init__()
        self._focus_id = 1
        self._on_resume = on_resume
        self.surfaceName = 'pause'
        self.buttonManager = ButtonManager()
        sz = GameState.__gsRenderOptions__.screenSize
        self.buttonManager.buttons.append(Button('resume', vec2(sz.x / 2, 300), Action(self.resume)))
        self.buttonManager.buttons.append(Button('quit', vec2(sz.x / 2, 360), Action(self.quit)))
        self.buttonManager.focus_on(0)
        self._button_count = self.buttonManager.button_count

    def update(self, args: GameArgs):
        self.buttonManager.update(args)

        if key_on_press(ki.down):
            cur = self.buttonManager.focus
            if cur < self._button_count - 1:
                self.buttonManager.focus_on(cur + 1)

        elif key_on_press(ki.up):
            cur = self.buttonManager.focus
            if cur != 0:
                self.buttonManager.focus_on(cur - 1)

    def draw(self, render_args: RenderArgs):
        self.buttonManager.draw(render_args)
        sz = GameState.__gsRenderOptions__.screenSize
        ResourceLib.Fonts.evil_empire.blit(render_args.target_surface, '>> Game Paused <<', vec2(sz.x / 2, 178))
