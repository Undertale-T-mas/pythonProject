__techAttackLevel__ = 0
__techDefenseLevel__ = 0


class TechData:
    @staticmethod
    def get_defense():
        return __techDefenseLevel__

    @staticmethod
    def get_normal_attack():
        return __techAttackLevel__
