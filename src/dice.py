from random import choice
import enum

class DiceValues(enum.StrEnum):
    RAY = 'Ray'
    HUMAN = 'Human'
    COW = 'Cow'
    CHICKEN = 'Chicken'
    TANK = 'Tank'

class Dice:

    def __init__(self, value: DiceValues):
        self.value = value

    def __repr__(self):
        return f'{self.value.value}'

    def __eq__(self, other):
        return self.value == other.value

    def save(self):
        return repr(self)

    @classmethod
    def load(cls, value: str):
        return cls(DiceValues(value))

    def roll(self):
        self.value = choice(
            [
                DiceValues.RAY,
                DiceValues.RAY,
                DiceValues.HUMAN,
                DiceValues.COW,
                DiceValues.CHICKEN,
                DiceValues.TANK,
            ]
        )

    def name(self):
        return f'{self.value.value}'
