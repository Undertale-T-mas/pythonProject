from core import *
from Resources import ResourceLib


class IButton(IUpdatable, IEntity):

    def on_focus(self):
        raise NotImplementedError()

    def on_click(self):
        raise NotImplementedError()

    def off_focus(self):
        raise NotImplementedError()


class ButtonManager(Entity):
    buttons: List[IButton]
    last_focus: IButton | None
    _focus_id: int

    def __init__(self):
        super().__init__()
        self.buttons = []
        self.last_focus = None
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

        if key_on_press(ki.confirm) and self.last_focus is not None:
            self.last_focus.on_click()

    def draw(self, render_args: RenderArgs):
        for but in self.buttons:
            but.draw(render_args)


class Button(Entity, IButton):

    _scale: float
    _text: str
    _on_click: Action

    def __init__(self, text: str, centre: vec2, on_click: Action):
        super().__init__()
        self.base_scale = 1.0
        self._on_click = on_click
        self._text = text
        self._scale = 1.0
        self.centre = centre
        self.text_font = ResourceLib.Fonts.pix0
        self.color = cv4.WHITE
        self._on_focus = False

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
        self._scale = Math.lerp(self._scale, 1.3 if self._on_focus else 1.0, args.elapsedSec * 15.0)

    def draw(self, render_args: RenderArgs):
        if self.image is not None:
            super().draw(render_args)
        self.text_font.blit(
            render_args.target_surface,
            ('>' + self._text + '<') if self._on_focus else self._text,
            self.centre, None, self.color, self._scale * self.base_scale
        )
