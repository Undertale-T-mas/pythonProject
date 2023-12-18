from pygame import mixer_music

from Core.GameObject import DelayedAction, Action
from Core.GameStates.GameState import instance_create
from Core.Physics.Easings import *


def stop_music(fade_out_sec: float = 1.0):
    mixer_music.fadeout(int(fade_out_sec * 1000))


def play_music(path: str, fade_out_sec: float = 1.0, fade_in_sec: float = 0.0):

    if mixer_music.get_busy():
        mixer_music.fadeout(int(fade_out_sec * 1000))

    if mixer_music.get_busy():

        mixer_music.load('Resources\\Audio\\Musics\\' + path)

        def act():
            mixer_music.play(1000, 0, int(fade_in_sec * 1000))

        instance_create(DelayedAction(fade_out_sec, Action(act)))

    else:

        def act():
            mixer_music.play(1000, 0, int(fade_in_sec * 1000))

        mixer_music.load('Resources\\Audio\\Musics\\' + path)
        instance_create(DelayedAction(0.0, Action(act)))
