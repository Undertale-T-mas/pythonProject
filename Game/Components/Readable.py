from typing import List

from Game.Map.Framework.Tiles import TILE_LENGTH
from Resources.ResourceLib import Fonts
from core import *


# noinspection PyMissingConstructor,PyTypeChecker
class Readable(Entity):
    __font__: GLFont
    __color__: Color
    __alpha__: float
    __updated__: bool
    __strLines__: List[str]
    __fontSize__: int
    __defaultFontSize__: int
    __strSurfs__: List[Surface]
    __lineDistance__: float
    __scale__: float

    def base_height(self) -> float:
        return self.__font__.get_height()

    def measure(self, s: str) -> vec2:
        l = s.split('\n')
        res = vec2(0, -self.__lineDistance__)

        for obj in l:
            res.y += self.lineDistance + self.__font__.get_height()
            res.x = max(res.x, self.__font__.measure_string(obj).x)

        return res

    @property
    def scale(self) -> float:
        return self.__scale__

    @scale.setter
    def scale(self, val: float):
        self.__scale__ = val

    def __init__(self, pos: vec2, _font: GLFont):
        super().__init__()
        self.__font__ = _font
        self.__scale__ = 1.0
        self.centre = pos
        self.__color__ = Color(255, 255, 255)
        self.__updated__ = True
        self.__strLines__ = ['']
        self.__alpha__ = 0.0
        self.__lineDistance__ = 0
        self.__fontSize__ = self.__defaultFontSize__ = Fonts.seek_size(self.__font__)

    def clear(self):
        self.__strLines__ = ['']
        self.__updated__ = True

    def update(self, args: GameArgs):
        pass

    @property
    def lineDistance(self):
        return self.__lineDistance__

    @lineDistance.setter
    def lineDistance(self, dist: float):
        self.__lineDistance__ = dist

    @property
    def color(self):
        return self.__color__

    @color.setter
    def color(self, val: Color | vec4):
        if isinstance(val, vec4):
            self.__color__ = Color(int(val.r / 255), int(val.g / 255), int(val.b / 255), int(val.a / 255))
            self.__updated__ = True
        else:
            self.__color__ = val
            self.__updated__ = True

    @property
    def alpha(self):
        return self.__alpha__

    @alpha.setter
    def alpha(self, val: float):
        self.__alpha__ = val
        self.__updated__ = True

    @property
    def font_size(self):
        return self.__fontSize__

    @font_size.setter
    def font_size(self, val: int):
        self.__fontSize__ = val
        self.__updated__ = True

    def push_str(self, s: str):
        self.__updated__ = True
        if '\n' in s:
            res = s.split()
        else:
            self.__strLines__[-1] += s
            return

        if len(res) == 0:
            self.__strLines__.append('')
            return

        self.__strLines__[-1] += res[0]
        for i in range(1, len(res)):
            self.__strLines__.append(res[i])

    def draw(self, render_args: RenderArgs):

        h = self.__font__.get_height()
        cur = vec2(self.centre.x, self.centre.y) - render_args.camera_delta
        for line in self.__strLines__:
            self.__font__.blit(
                render_args.target_surface, line,
                cur, col=vec4.from_color(self.__color__) * self.__alpha__,
                scale=self.scale
            )
            cur.y += self.lineDistance + h


class PanelBoard(Entity):
    def __init__(self, pos: vec2, font_base_height: float, size: vec2):
        super().__init__()
        self.__alpha__ = 0.0
        self.image = SingleImage('Effects\\Text\\panel.png')
        self.image.__alpha__ = 0.0
        self.image.scale = vec2((size.x + 55) / self.image.imageSource.get_width(), (size.y + 30) / self.image.imageSource.get_height())
        self.centre = pos + vec2(0, (size.y - font_base_height) / 2)

    def clear(self):
        pass

    __alpha__: float

    @property
    def alpha(self) -> float:
        return self.__alpha__

    @alpha.setter
    def alpha(self, val: float):
        self.__alpha__ = val
        self.image.alpha = self.__alpha__

    def draw(self, render_args: RenderArgs):
        super().draw(render_args)


class PanelText(Entity):
    text: Readable
    panel: PanelBoard
    __restStr__: str
    __fullStr__: str
    __timeTot__: float
    __putTime__: float
    __boardAlphaMax__: float
    __textAlphaMax__: float
    __presentTime__: float

    __enabled__: bool

    def __init__(self, text: str, pos: vec2, _font: Font | None = None, put_speed: float = 60.0, alpha_change_time = 0.6, text_alpha_max: float = 1.0, board_alpha_max = 1.0):
        super().__init__()
        if _font is None:
            _font = Fonts.glitch_goblin
        pos -= vec2(0, TILE_LENGTH)
        self.text = Readable(pos, _font)
        size = self.text.measure(text)
        pos.y -= size.y
        self.text.centre = pos
        self.panel = PanelBoard(pos, self.text.base_height(), size)
        self.__restStr__ = self.__fullStr__ = text
        self.__enabled__ = False
        self.__presentTime__ = alpha_change_time
        self.__boardAlphaMax__ = board_alpha_max
        self.__textAlphaMax__ = text_alpha_max
        self.__timeTot__ = 0.0
        self.__putTime__ = 1 / put_speed
        self.__onToggling__ = False
        self.__alpha__ = 0.0

    def clear(self):
        self.text.clear()
        self.panel.clear()

    @property
    def enabled(self) -> bool:
        return self.__enabled__

    __onToggling__: bool
    __alpha__: float

    @property
    def alpha(self) -> float:
        return self.__alpha__

    @alpha.setter
    def alpha(self, val: float):
        self.__alpha__ = val
        self.text.alpha = val * self.__textAlphaMax__
        self.panel.alpha = val * self.__boardAlphaMax__

    def __set_toggling_false__(self):
        self.__onToggling__ = False
        if self.enabled:
            self.alpha = 1.0
        else:
            self.alpha = 0
            self.clear()

    def appear(self):
        if self.__onToggling__:
            return
        if self.__enabled__:
            return
        self.__restStr__ = self.__fullStr__
        self.__onToggling__ = True
        self.__enabled__ = True

        def modify_alpha(val: float):
            self.alpha = val

        instance_create(DelayedAction(self.__presentTime__, Action(self.__set_toggling_false__)))
        EasingRunner(self.__presentTime__, 0.0, 1.0, EaseType.cubic).run(modify_alpha)

    def disappear(self):
        if self.__onToggling__:
            return
        if not self.__enabled__:
            return
        self.__enabled__ = False
        self.__onToggling__ = True

        def modify_alpha(val: float):
            self.alpha = val

        instance_create(DelayedAction(self.__presentTime__, Action(self.__set_toggling_false__)))
        EasingRunner(self.__presentTime__, 1.0, 0.0, EaseType.quint).run(modify_alpha)

    def update(self, args: GameArgs):
        if not self.enabled:
            return

        if len(self.__restStr__) > 0:
            if self.__onToggling__:
                self.__timeTot__ += args.elapsedSec * 0.85
            else:
                self.__timeTot__ += args.elapsedSec
            while self.__timeTot__ >= self.__putTime__:
                self.__timeTot__ -= self.__putTime__
                self.text.push_str(self.__restStr__[0])
                self.__restStr__ = self.__restStr__[1:]
                if len(self.__restStr__) == 0:
                    break

        self.text.update(args)

    def draw(self, render_args: RenderArgs):
        # super().draw(render_args)
        self.panel.draw(render_args)
        self.text.draw(render_args)