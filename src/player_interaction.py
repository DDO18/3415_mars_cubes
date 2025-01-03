from abc import ABC, abstractmethod

class PlayerInteraction(ABC):
    @classmethod
    @abstractmethod
    def choose_dice(cls, remaining_dice):
        pass
