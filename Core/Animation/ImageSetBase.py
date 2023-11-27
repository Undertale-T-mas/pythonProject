import io
import os
from typing import *

import pygame
from pygame import *
from pygame import Vector2 as vec2
from pygame.transform import rotate

import Resources.ResourceLoad
from Core.Animation.AnchorBase import Anchor
from Core.GameArgs import *
from Resources.ResourceLoad import *


class ImageSetBase:

    def load(self, path: str):
        self.imageSource = load_image(path)

    imageSource: Surface
    blockSize: vec2
    indexX: int = 0
    indexY: int = 0
    scale: float = 1.0

    anchor: Anchor

    def source_area(self) -> Rect:
        raise NotImplementedError()

    def draw_self(self, args: RenderArgs, centre: vec2):
        r = self.source_area()
        v = centre - self.anchor.get_anchor_pos() * self.scale

        transform.scale()

        args.target_surface.blit(
            self.imageSource,
            v,
            r
        )
