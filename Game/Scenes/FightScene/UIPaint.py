from Core.Animation.Animation import Animation
from Core.GameStates.Scene import *
from Core.GameStates import *
import Core.GameStates.GameState
from Core.GameStates.GameState import *
from Core.Physics.Easings import *
from Game.Characters.Humans.Player import Player, PlayerData
from Game.Characters.Movable import DeathAnimation
from Game.Map.Framework.TileMap import *
from Game.Scenes.TileMapScene import *
from Resources.ResourceLib import Fonts


class UIPainter(Entity):
    black_canvas: RenderTarget

    __HPLIST__ = [30, 20, 20, 1]

    def __init__(self):
        super().__init__()
        self.surfaceName = 'bg'
        self.black_canvas = RenderTarget(GameState.__gsRenderOptions__.screenSize.x, 72)
        self.old_hp = self.old_cooldown = 0
        self.old_cooldown = -1
        wsur = Surface(vec2(1, 1))
        wsur.set_at((0, 0), (255, 255, 255, 255))
        self.pix = Texture(wsur)
        self.updated = True
        self.bullet_tex = Texture(load_image('Objects\\Icons\\Bullet.png'))
        self.sc_tex = Texture(load_image('Objects\\Icons\\CrystalBlue.png'), GL_LINEAR)
        self.is_dead = False
        self.recharge_timer = 0.0
        self.alpha = 0.9
        self.old_scnt = 0

    old_hp: float
    old_ammunition: int
    old_scnt: int
    old_cooldown: float
    pix: Texture
    max_hp: float
    old_dif: int
    alpha: float
    recharge_time: float
    bullet_tex: Texture
    sc_tex: Texture

    data: PlayerData

    updated: bool
    is_dead: bool
    recharge_timer: float

    def dead(self):
        self.updated = True
        self.is_dead = True

    def update(self, args: GameArgs):
        self.data = get_player_data()
        if self.is_dead:
            self.alpha = Math.lerp(self.alpha, 1.0, args.elapsedSec * 10)
            self.updated = True

        if (self.data.hp != self.old_hp or self.old_cooldown != self.data.fire_cooldown
                or self.old_ammunition != self.data.ammunition or self.old_dif != self.data.difficulty
                or self.old_scnt != self.data.player_object.save_slot_energy()
            ):
            self.old_hp = self.data.hp
            self.old_ammunition = self.data.ammunition
            self.updated = True
            self.old_cooldown = self.data.fire_cooldown
            self.old_dif = self.data.difficulty
            self.old_scnt = self.data.player_object.save_slot_energy()
            self.max_hp = UIPainter.__HPLIST__[self.data.difficulty]

            self.recharge_time = self.data.player_object.recharge_time()
            self.recharge_timer = self.data.fire_cooldown

    def blit(self, sur: RenderTarget, y_limit: float = 0.0):

        if self.updated:

            self.black_canvas.clear(vec4(0.6, 0.6, 0.6, self.alpha))

            # self.black_canvas.clear(vec4(1.0, 0.0, 0.0, 1))

            sz = vec2(GameState.__gsRenderOptions__.screenSize.x, 72)

            # draw line at the bottom:
            glUseProgram(0)
            glColor4f(0.2, 0.160, 0.2, 1.0)
            glLineWidth(5)
            glBegin(GL_LINES)
            glVertex2f(0, sz.y - 2)
            glVertex2f(sz.x, sz.y - 2)
            glEnd()

            # draw hp bar:

            self.black_canvas.blit_data(self.pix, RenderData(
                vec2(190, 35), scale=vec2(190, 39),
                color=vec4(0.6, 0.0, 0.0, 1.0) if self.is_dead else vec4(1, 0.0, 0.13, 1.0),
                anchor=vec2(0.5, 0.5)
            ))
            hp_scale = 1 - self.old_hp / self.max_hp
            if not self.is_dead and hp_scale > 0.001:
                self.black_canvas.blit_data(self.pix, RenderData(
                    vec2(285 - 95 * hp_scale, 35), scale=vec2(190 * hp_scale, 39),
                    color=vec4(0.6, 0.0, 0.0, 1.0),
                    anchor=vec2(0.5, 0.5)
                ))

            self.black_canvas.blit_data(self.pix, RenderData(
                vec2(571, 51), scale=vec2(160, 12),
                color=vec4(0.7, 0.3, 0.13),
                anchor=vec2(0.5, 0.5)
            ))
            if self.recharge_timer > 0.0001:
                rec_scale = self.recharge_timer / self.recharge_time
                self.black_canvas.blit_data(self.pix, RenderData(
                    vec2(651 - 80 * rec_scale, 51), scale=vec2(160 * rec_scale, 12),
                    color=cv4.BROWN,
                    anchor=vec2(0.5, 0.5)
                ))

            f = Fonts.pix0
            f.blit(self.black_canvas, 'HP', vec2(50, 34), col=cv4.WHITE, scale=0.9)
            f.blit(self.black_canvas, 'BULLET', vec2(400, 34), col=cv4.WHITE, scale=0.8)

            f.blit(self.black_canvas, 'SAVE', vec2(740, 34), col=cv4.WHITE, scale=0.8)

            if self.is_dead:
                f.blit(self.black_canvas, 'DEAD', vec2(190, 34),
                       col=vec4(0.9, 0.9, 0.9), scale=0.75)
            else:
                f.blit(self.black_canvas, str(int(self.old_hp + 0.999)) + '/' + str(self.max_hp), vec2(190, 34), col=cv4.WHITE, scale=0.75)

            pos = vec2(511, 34)
            for i in range(self.old_ammunition):
                self.black_canvas.blit_data(self.bullet_tex, RenderData(pos, anchor=self.bullet_tex.centre))
                pos.x += 20

            for i in range(self.old_ammunition + 1, 8):
                self.black_canvas.blit_data(self.bullet_tex, RenderData(pos, anchor=self.bullet_tex.centre, color=cv4.SILVER))
                pos.x += 20

            pos = vec2(841, 32)
            for i in range(self.old_scnt):
                self.black_canvas.blit_data(self.sc_tex, RenderData(pos, anchor=self.sc_tex.centre))
                pos.x += 51

            for i in range(self.old_scnt + 1, self.data.player_object.save_slot_size() + 1):
                self.black_canvas.blit_data(self.sc_tex, RenderData(pos, anchor=self.sc_tex.centre, color=cv4.SILVER))
                pos.x += 51

        sur.blit(self.black_canvas, vec2(0, y_limit),
                 FRect(0, min(y_limit, 72.0), self.black_canvas.get_width(),
                       Math.clamp(72.0 - y_limit, 0, 72)))


