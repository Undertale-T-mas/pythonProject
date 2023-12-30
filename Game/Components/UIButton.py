from Resources.ResourceLib import Sounds
from core import *
from Resources import ResourceLib


class IButton(IUpdatable, IEntity):

    @property
    def show_enable(self):
        raise NotImplementedError()

    @show_enable.setter
    def show_enable(self, val: bool):
        raise NotImplementedError()

    @property
    def pos_delta(self):
        raise NotImplementedError()

    @pos_delta.setter
    def pos_delta(self, delta: vec2):
        raise NotImplementedError()

    @property
    def alpha(self):
        raise NotImplementedError()

    @alpha.setter
    def alpha(self, alp: vec2):
        raise NotImplementedError()

    def on_focus(self):
        raise NotImplementedError()

    def on_click(self):
        raise NotImplementedError()

    def off_focus(self):
        raise NotImplementedError()


class IHandlerUI:
    def on_activate(self):
        raise NotImplementedError()

    def on_deactivate(self):
        raise NotImplementedError()

    def receive(self, data: Any):
        raise NotImplementedError()


class ButtonManager(Entity, IHandlerUI):
    buttons: List[IButton]
    last_focus: IButton | None
    _focus_id: int
    _alpha: float

    _tar_alpha: float
    _tar_pos: vec2
    _activate: bool
    show_enable: bool
    _appear_delta: vec2

    @property
    def delta(self):
        return self.centre

    @property
    def appear_delta(self):
        return self._appear_delta

    @appear_delta.setter
    def appear_delta(self, val: vec2):
        self._appear_delta = val

    def on_activate(self):
        self._activate = True
        self.centre = self._appear_delta
        self._tar_pos = vec2(0.0, 0.0)
        self._tar_alpha = 1.0
        self._alpha = 0.0

    def on_deactivate(self):
        self._activate = False
        self._tar_pos = self._appear_delta
        self._tar_alpha = 0.5

    def receive(self, data: Any):
        self.centre = data

    def __init__(self):
        super().__init__()
        self.buttons = []
        self._activate = False
        self._appear_delta = vec2(-200.0, 0.0)
        self.last_focus = None
        self.show_enable = False
        self._focus_id = 0

    def focus_on(self, _id: int):
        if self.last_focus is not None:
            self.last_focus.off_focus()
        self.last_focus = self.buttons[_id]
        self.buttons[_id].on_focus()
        self._focus_id = _id

    @property
    def focus(self) -> int:
        return self._focus_id

    @property
    def button_count(self):
        return len(self.buttons)

    def update(self, args: GameArgs):
        for but in self.buttons:
            but.update(args)

        self.centre = Math.lerp(
            self.centre,
            self._tar_pos,
            args.elapsedSec * 20.0
        )
        self._alpha = Math.lerp(
            self._alpha,
            self._tar_alpha,
            args.elapsedSec * 20.0
        )
        if self._activate:
            if key_on_press(ki.confirm) and self.last_focus is not None:
                self.last_focus.on_click()
                Sounds.uiSelect.play()

    def draw(self, render_args: RenderArgs):
        for but in self.buttons:
            but.show_enable = self.show_enable
            but.pos_delta = self.centre
            but.alpha = self._alpha
            but.draw(render_args)


class Button(Entity, IButton):

    _scale: float
    _text: str
    _on_click: Action
    _pos_delta: vec2
    _show_enable: bool
    _pos_base: vec2

    def __init__(self, text: str, centre: vec2, on_click: Action):
        super().__init__()
        self._pos_delta = vec2(0.0, 0.0)
        self.base_scale = 1.0
        self._on_click = on_click
        self._text = text
        self._scale = 1.0
        self._show_enable = True
        self._pos_base = centre
        self._alpha = 0.0
        self.text_font = ResourceLib.Fonts.pix0
        self.color = cv4.WHITE
        self._on_focus = False

    _alpha: float

    @property
    def show_enable(self):
        return self._show_enable

    @show_enable.setter
    def show_enable(self, val: bool):
        self._show_enable = val

    @property
    def pos_delta(self):
        return self._pos_delta

    @pos_delta.setter
    def pos_delta(self, delta: vec2):
        self._pos_delta = delta

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alp: vec2):
        self._alpha = alp

    base_scale: float
    text_font: GLFont
    color: vec4

    def change_text(self, text: str):
        self._text = text

    @property
    def back_image(self):
        return self.image

    @back_image.setter
    def back_image(self, val: ImageSetBase):
        self.image = val

    def on_click(self):
        self._on_click.act()

    _on_focus: bool

    def on_focus(self):
        self._on_focus = True

    def off_focus(self):
        self._on_focus = False

    def update(self, args: GameArgs):
        self.centre = self._pos_base + self._pos_delta
        self._scale = Math.lerp(self._scale, 1.3 if self._on_focus else 1.0, args.elapsedSec * 15.0)

    def draw(self, render_args: RenderArgs):
        if self.image is not None:
            super().draw(render_args)
        if self._show_enable:
            text = ('>' + self._text + '<') if self._on_focus else self._text
        else:
            text = self._text
        self.text_font.blit(
            render_args.target_surface,
            text,
            self.centre, None, self.color * vec4(1.0, 1.0, 1.0, self._alpha),
            self._scale * self.base_scale
        )
