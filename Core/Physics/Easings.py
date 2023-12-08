import builtins
from enum import Enum
from math import *

import Core.GameStates.GameState
from Core.GameObject import *

T = TypeVar("T", bound=Union[float, vec2])


class EasingArgs:
    time: float
    position: vec2

    def __init__(self, _time: float, pos: vec2):
        self.time = _time
        self.position = pos


class EasingFunc(Generic[T]):
    calcFunc: classmethod | staticmethod

    def __init__(self, method):
        self.calcFunc = method

    def calc(self, args: EasingArgs) -> T:
        return self.calcFunc(args)


class Easing(Generic[T]):
    start: T
    end: T | None
    time: float
    func: EasingFunc

    def __init__(self, _time: float, start: T, end: T | None, func: EasingFunc):
        self.start = start
        self.end = end
        self.time = _time
        self.func = func

    def chop(self, _time: float):
        old_func = self.func
        result = Easing(
            self.time, self.start, self.end,
            EasingFunc(lambda args: old_func.calc(EasingArgs(args.time + _time, args.position)))
        )
        return result


class EaseType(Enum):
    linear = 0,
    sine = 1,
    quad = 2,
    cubic = 3,
    quart = 4,
    quint = 5,
    expo = 6,
    circ = 7,
    back = 8,
    elastic = 9,
    bounce = 10


def ease_out_bounce(x: float) -> float:
    if x < 1 / 2.75:
        return 7.5625 * x * x
    elif x < 2 / 2.75:
        x -= 1.5 / 2.75
        return 7.5625 * x * x + 0.75
    elif x < 2.5 / 2.75:
        x -= 2.25 / 2.75
        return 7.5625 * x * x + 0.9375
    else:
        x -= 2.625 / 2.75
        return 7.5625 * x * x + 0.984375


__defaultEaseFuncs__ = {
    EaseType.linear: lambda x: x,
    EaseType.sine: lambda x: Math.sin(x * pi / 2),
    EaseType.quad: lambda x: x * x,
    EaseType.cubic: lambda x: x * x * x,
    EaseType.quart: lambda x: x ** 4,
    EaseType.quint: lambda x: x ** 5,
    EaseType.expo: lambda x: 0 if abs(x) < 1e-9 else 2 ** (10 * x - 10),
    EaseType.circ: lambda x: 1 - sqrt(1 - x * x),
    EaseType.back: lambda x: 2.70158 * x * x * x - 1.70158 * x * x,
    EaseType.elastic: lambda x: 0 if abs(x) < 1e-9 else -(2 ** (10 * x - 10)) * sin((x * 10 - 10.75) * 2 * pi / 3),
    EaseType.bounce: lambda x: 1 - ease_out_bounce(1 - x)
}


class EasingGenerator(Generic[T]):
    @staticmethod
    def generate(_time: float, start: T, end: T, ease_type: EaseType = EaseType.linear):
        return Easing(_time, start, end, EasingFunc(
            lambda args: start + (end - start) * __defaultEaseFuncs__[ease_type](args.time / time)))

    @staticmethod
    def stable(_time: float, val: T):
        return Easing(_time, val, val, EasingFunc(lambda args: val))

    @staticmethod
    def linear(start: T, speed: T):
        return Easing(1e20, start, None,
                      EasingFunc(lambda args: start + vec2(args.time * speed.x, args.time * speed.y)))

    @staticmethod
    def sin(intensity: float, cycle: float, phase: float):
        return Easing(1e20, Math.sin(phase / 180 * pi), None,
                      EasingFunc(lambda args: intensity * Math.sin((phase + args.time) / 180 * pi / cycle)))

    @staticmethod
    def combine(source_x: Easing, source_y: Easing):
        return Easing(
            max(source_x.time, source_y.time),
            vec2(source_x.start, source_y.start),
            vec2(source_x.end, source_y.end),
            EasingFunc(lambda args: vec2(source_x.func.calc(args), source_y.func.calc(args)))
        )


class VirtualEasingObject(GameObject, Generic[T]):
    easeIndex = 0
    timeProgress = 0
    result: T
    easings: List[Easing]
    follow: Entity | None
    action: Any

    def __init__(self, action, easings: List[Easing], follow: Entity | None):
        self.easings = easings
        self.follow = follow
        self.action = action

    def update(self, args: GameArgs):
        self.timeProgress += args.elapsedSec
        if self.timeProgress >= self.easings[self.easeIndex].time:
            self.timeProgress -= self.easings[self.easeIndex].time
            self.easeIndex += 1
        if self.easeIndex >= len(self.easings):
            self.dispose()
            return
        if self.follow is None:
            pos = vec2(0, 0)
        else:
            if self.is_disposed():
                self.dispose()
                return
            pos = self.follow.centre
        result = self.easings[self.easeIndex].func.calc(EasingArgs(self.timeProgress, pos))
        self.action(result)


class EasingRunner(Generic[T]):
    easings: List[Easing]

    def __init__(self, _time: float, start: T | None = None, end: T | None = None,
                 ease_args: EaseType | Easing = EaseType.linear):
        if T == float:
            if start is None:
                start = 0
            if end is None:
                end = 0
        else:
            if start is None:
                start = vec2(0, 0)
            if end is None:
                end = vec2(0, 0)

        if isinstance(ease_args, EaseType):
            self.easings = [EasingGenerator.generate(_time, start, end, ease_args)]
        else:
            self.easings = [ease_args]

    def to(self, _time: float, tar: T, ease_type: EaseType = EaseType.linear):
        front = self.easings[-1]
        self.easings.append(EasingGenerator.generate(_time, front.end, tar, ease_type))
        return self

    def combine_y(self, easing: Easing, effect_from: int = 0, effect_to: int = -1):
        if effect_to < 0:
            effect_to = len(self.easings) + effect_to

        tot = 0
        for i in range(effect_from, effect_to + 1):
            self.easings[i] = EasingGenerator.combine(self.easings[i], easing.chop(tot))
            tot += self.easings[i].time

    def combine_x(self, easing: Easing, effect_from: int = 0, effect_to: int = -1):
        if effect_to < 0:
            effect_to = len(self.easings) + effect_to

        tot = 0
        for i in range(effect_from, effect_to + 1):
            self.easings[i] = EasingGenerator.combine(easing.chop(tot), self.easings[i])
            tot += self.easings[i].time

    def run(self, action, follow: Entity | None = None):
        Core.GameStates.GameState.instance_create(VirtualEasingObject(action, self.easings, follow))
