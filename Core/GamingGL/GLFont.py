from pygame.font import Font

from Core.GamingGL.GLBase import *


class TexChar:
    __char__: str
    __size__: vec2
    __tex__: Texture

    def __init__(self, ch: str, tex: Texture):
        self.__tex__ = tex
        self.__size__ = vec2(tex.width, tex.height)
        self.__char__ = ch

    @property
    def char(self):
        return self.__char__

    @property
    def texture(self):
        return self.__tex__

    @property
    def size(self):
        return self.__size__


class GlyphGenerator:
    __font__: Font
    glyph_set: Dict[str, TexChar]
    __text_height__: float

    def __init__(self, font: Font):
        self.glyph_set = dict()
        self.__font__ = font
        self.__text_height__ = font.get_height()

    def get_glyph(self, ch: str):
        if len(ch) >= 2:
            raise ArgumentError()

        if ch in self.glyph_set:
            return self.glyph_set[ch]

        res = TexChar(ch, Texture(self.__font__.render(ch, True, [255, 255, 255, 255])))
        self.glyph_set[ch] = res
        return res

    def measure_string(self, s: str):
        y = self.__text_height__
        x = 0

        for ch in s:
            if ch == '\n':
                raise ArgumentError()
            x += self.get_glyph(ch).size.x

        return vec2(x, y)


class GLFont:

    __height__: float
    __font__: Font
    __glyph_set__: GlyphGenerator

    @property
    def base_font(self) -> Font:
        return self.__font__

    def blit(self, target: IRenderTarget, text: str, centre: vec2, anchor: vec2 | None = None, col: vec4 = vec4(1.0, 1.0, 1.0, 1.0), scale: float = 1.0):
        if anchor is None:
            anchor = self.__glyph_set__.measure_string(text) / 2.0

        anchor *= scale
        loc = vec2(centre.x - anchor.x, centre.y - anchor.y)

        target.set_target_self()

        for ch in text:
            if ch == '\n':
                raise ValueError()
            glyph = self.__glyph_set__.get_glyph(ch)
            glyph.texture.draw(RenderData(loc, col, vec2(scale, scale), False, vec2(0, 0)))
            loc.x += glyph.size.x

    def __init__(self, font: Font):
        self.__font__ = font
        self.__glyph_set__ = GlyphGenerator(self.__font__)
        self.__height__ = font.get_height()

    def get_height(self):
        return self.__height__

    def measure_string(self, s: str) -> vec2:
        return self.__glyph_set__.measure_string(s)

