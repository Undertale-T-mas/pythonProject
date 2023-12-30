from typing import Any, List

from Core.GameArgs import GameArgs


class Action:
    __fun__: staticmethod | classmethod

    def __init__(self, fun):
        self.__fun__ = fun

    def act(self):
        return self.__fun__()


class ArgAction:
    __fun__: staticmethod | classmethod

    def __init__(self, fun):
        self.__fun__ = fun

    def act(self, *args) -> Any:
        return self.__fun__(*args)


class IUpdatable:

    def update(self, args: GameArgs):
        raise NotImplementedError()

    def is_disposed(self):
        raise NotImplementedError()


class GameObject(IUpdatable):
    def __init__(self):
        self._focus_id = 0

    __disposed__ = False
    _focus_id: int

    @property
    def focus_id(self):
        return self._focus_id

    def is_disposed(self):
        return self.__disposed__

    def dispose(self):
        self.__disposed__ = True


class StableAction(GameObject):
    __action__: Action
    __time__: float

    def __init__(self, _time: float, action: Action):
        self.__time__ = _time
        super().__init__()
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
        super().__init__()
        self.__action__ = action

    def update(self, args: GameArgs):
        self.__delay__ -= args.elapsedSec
        if self.__delay__ <= 0:
            self.dispose()
            self.__action__.act()


class TimeLine(GameObject):

    times: List[float]
    events: List[Action]

    cur_time: float
    idx: int

    def __init__(self):
        self.times = []
        self.events = []
        self.cur_time = 0.0
        self.idx = 0
        super().__init__()

    def update(self, args: GameArgs):
        self.cur_time += args.elapsedSec
        while self.idx < len(self.events) and self.cur_time >= self.times[self.idx]:
            self.events[self.idx].act()
            self.idx += 1

    def insert(self, time: float, action: Action):
        self.times.append(time)
        self.events.append(action)
