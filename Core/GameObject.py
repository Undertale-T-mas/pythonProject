from Core.GameArgs import GameArgs


class Action:
    __fun__: staticmethod | classmethod

    def __init__(self, fun):
        self.__fun__ = fun

    def act(self):
        self.__fun__()


class ArgAction:
    __fun__: staticmethod | classmethod

    def __init__(self, fun):
        self.__fun__ = fun

    def act(self, *args):
        self.__fun__(*args)


class GameObject:
    def update(self, args: GameArgs):
        raise NotImplementedError()

    __disposed__ = False

    def is_disposed(self):
        return self.__disposed__

    def dispose(self):
        self.__disposed__ = True


class StableAction(GameObject):
    __action__: Action
    __time__: float

    def __init__(self, _time: float, action: Action):
        self.__time__ = _time
        self.__action__ = action

    def update(self, args: GameArgs):
        self.__time__ -= args.elapsedSec
        if self.__time__ <= 0:
            self.dispose()
            return

        self.__action__.act()


class DelayedAction(GameObject):
    __action__: Action
    __delay__: float

    def __init__(self, delay: float, action: Action):
        self.__delay__ = delay
        self.__action__ = action

    def update(self, args: GameArgs):
        self.__delay__ -= args.elapsedSec
        if self.__delay__ <= 0:
            self.dispose()
            self.__action__.act()

