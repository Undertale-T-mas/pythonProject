__techAttackLevel__ = 0
__techDefenseLevel__ = 0
__techSaveSlot__ = 3
__techSaveCost__ = 2


class TechData:
    @staticmethod
    def get_defense():
        return __techDefenseLevel__

    @staticmethod
    def get_normal_attack():
        return __techAttackLevel__

    @staticmethod
    def get_save_slot():
        return __techSaveSlot__

    @staticmethod
    def get_save_cost():
        return __techSaveCost__
