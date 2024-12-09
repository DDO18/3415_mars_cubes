from random import *

from src.player_interaction import PlayerInteraction

class Bot(PlayerInteraction):

    @classmethod
    def choose_dice(cls, remaining_dice):
        return choice(remaining_dice)
