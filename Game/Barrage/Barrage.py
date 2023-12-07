from Core.Animation.Anchor import *
from Core.Animation.AnchorBase import *
from Core.Animation.ImageSetBase import *
from Core.Animation.ImageSet import *
from Core.GameStates.Scene import *
import Core.GameStates.GameStates
from Core.GameStates.ObjectManager import *
from Core.Physics.Easings import *
from Core.Physics.PhysicSurface import *
from Core.Physics.PhysicManager import *
from Core.Physics.Collidable import *
from Core.Physics.CollidingArea import *
from Core.Render.RenderOptions import *
from Core.Render.SurfaceManager import *
from Core.Render.VSurface import *
from Core.GameObject import *
from Core.GameArgs import *
from pygame import Vector2 as vec2
from pygame import *


class Barrage(Entity, Collidable):
    autoDispose: bool = False

    def __set_centre__(self, result: vec2):
        self.centre = result
        self.physicSurfName = 'barrage'
        self.surfaceName = 'barrage'

    def move(self, ease: EasingRunner | Easing):
        if isinstance(ease, Easing):
            ease = EasingRunner(ease.time, ease.start, ease.end, ease)
        ease.run(self.__set_centre__, self)

    def update(self, args: GameArgs):
        if self.centre.x < -200 or self.centre.x > GameStates.__gsRenderOptions__.screenSize.x:
            self.dispose()
        if self.centre.y < -200 or self.centre.y > GameStates.__gsRenderOptions__.screenSize.y:
            self.dispose()

