from Game.Characters.Humans.Data import IPlayer
from Resources.ResourceLib import Sounds
from core import *
from Game.Tech.DataLib import TechData


SAVE_HOLD_TIME = 2.0


class SavingSlot(GameObject):

    count: Savable[int]
    objSource: IPlayer

    def __init__(self, obj_source: IPlayer):
        super().__init__()
        self.count = Savable('player\\item.save_crystal', 0)
        self.__saveTimeTot__ = 0.0
        self.objSource = obj_source

    def player_moved(self):
        self.__saveTimeTot__ = 0.0

    def slot_size(self) -> int:
        return TechData.get_save_slot()

    def acceptable(self) -> bool:
        return self.count.value < self.slot_size()

    def push(self):
        self.count.value += 1

    def usable(self):
        return self.count.value >= TechData.get_save_cost()

    def use(self):
        if not self.usable():
            raise ValueError()
        self.count.value -= TechData.get_save_cost()

    __saveTimeTot__: float

    def progress(self):
        return self.__saveTimeTot__ / SAVE_HOLD_TIME

    def update(self, args: GameArgs):
        if self.usable() and key_hold(KeyIdentity.ctrl) and key_hold(KeyIdentity.save):
            self.__saveTimeTot__ += args.elapsedSec

        else:
            self.__saveTimeTot__ = 0.0

        if self.__saveTimeTot__ >= SAVE_HOLD_TIME:
            self.__saveTimeTot__ = 0.0
            self.use()
            self.objSource.crystal_save()
            Sounds.save.play()

