from copy import copy

from src.dice import Dice, DiceValues
from src.player import Player


class GameState:
    NUMBER_OF_DICES = 13

    def __init__ (self, players: list[Player], player: int = 0, remaining_dice: list[str] = None, chosen_dice: list[str] = None):
        self.players = players
        self.player = player

        if remaining_dice is None: self.remaining_dice = []
        else: self.remaining_dice = [Dice.load(dice) for dice in remaining_dice]

        if chosen_dice is None: self.chosen_dice = []
        else: self.chosen_dice = [Dice.load(dice) for dice in chosen_dice]

    def __eq__(self, other):
        return(
            self.players == other.players
            and self.player == other.player
            and self.remaining_dice == other.remaining_dice
            and self.chosen_dice == other.chosen_dice
        )

    def save(self):
        return {
            "player": self.player,
            "remaining_dice": [dice.save() for dice in self.remaining_dice],
            "chosen_dice": [dice.save() for dice in self.chosen_dice],
            "players": [player.save() for player in self.players]
        }

    @classmethod
    def load(cls, data: dict):
        return cls(
            players = [Player.load(player) for player in data["players"]],
            player = data["player"],
            remaining_dice = data["remaining_dice"],
            chosen_dice = data["chosen_dice"],
        )

    def current_player(self):
        return self.players[self.player]

    def next_player(self):
        self.player += 1
        self.player %= len(self.players)

    def reroll(self):
        for dice in self.remaining_dice:
            dice.roll()

    def prepare_new_dices(self):
        self.remaining_dice = [Dice() for _ in range(self.NUMBER_OF_DICES)]
        self.chosen_dice = []

    def can_choose_dice(self, dice: Dice):
        return dice not in self.chosen_dice or dice in [DiceValues.RAY, DiceValues.TANK]

    def choose_dice(self, dice: Dice):
        assert(self.can_choose_dice(dice))
        dice_count = self.remaining_dice.count(dice)
        while dice_count != 0:
            self.chosen_dice.append(copy(dice))
            self.remaining_dice.remove(dice)
            dice_count -= 1

    def add_score(self):
        rays = self.chosen_dice.count(DiceValues.RAY)
        humans = self.chosen_dice.count(DiceValues.HUMAN)
        cows = self.chosen_dice.count(DiceValues.COW)
        chickens = self.chosen_dice.count(DiceValues.CHICKEN)
        tanks = self.chosen_dice.count(DiceValues.TANK)

        if tanks > rays:
            return 0

        set_bonus = (3 if humans and chickens and cows else 0)

        return humans + cows + chickens + set_bonus
