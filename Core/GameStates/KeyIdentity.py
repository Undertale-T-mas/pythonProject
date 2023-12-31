from enum import Enum

import pygame


class KeyIdentity(Enum):
    confirm = [pygame.K_z, pygame.K_KP_ENTER, pygame.KSCAN_KP_ENTER, pygame.K_RETURN]
    shoot = [pygame.K_SPACE, pygame.K_j]
    recharge = [pygame.K_r]

    left = [pygame.K_a, pygame.K_LEFT]
    right = [pygame.K_d, pygame.K_RIGHT]
    down = [pygame.K_s, pygame.K_DOWN]
    up = [pygame.K_w, pygame.K_UP]
    jump = [pygame.K_c, pygame.K_UP, pygame.K_w]

    speed_0 = [pygame.K_0]
    speed_1 = [pygame.K_1]
    speed_2 = [pygame.K_2]
    speed_3 = [pygame.K_3]
    speed_4 = [pygame.K_4]
    speed_5 = [pygame.K_5]
    speed_6 = [pygame.K_6]
    speed_7 = [pygame.K_7]
    speed_8 = [pygame.K_8]
    speed_9 = [pygame.K_9]

    ctrl = [pygame.K_LCTRL]
    save = [pygame.K_s]

    pause = [pygame.K_ESCAPE]
    delete = [pygame.K_BACKSPACE]
    enter = [pygame.K_KP_ENTER, pygame.K_RETURN]
