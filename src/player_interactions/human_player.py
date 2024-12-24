from src.player_interaction import PlayerInteraction

from src.dice import Dice, DiceValues

class Human(PlayerInteraction):

    @classmethod
    def choose_dice(cls, remaining_dice):
        dice = DiceValues(input('Выберите кубик: '))
        return Dice(dice)
