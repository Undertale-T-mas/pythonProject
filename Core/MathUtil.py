import math


class Math:
    @staticmethod
    def sin(val: float) -> float:
        return math.sin(val)

    @staticmethod
    def abs(val: float) -> float:
        if val > 0:
            return val
        return -val
