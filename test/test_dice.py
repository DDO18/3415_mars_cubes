import pytest

from src.dice import Dice, DiceValues


def test_init():
    dice1 = Dice(DiceValues.RAY)
    dice2 = Dice(DiceValues.HUMAN)
    dice3 = Dice(DiceValues.TANK)
    assert dice1.value == 'Ray'
    assert dice2.value == 'Human'
    assert dice3.value == 'Tank'

def test_eq():
    dice1 = Dice(DiceValues.RAY)
    dice2 = Dice(DiceValues.RAY)
    dice3 = Dice(DiceValues.HUMAN)
    dice4 = Dice(DiceValues.TANK)
    assert dice1 == dice2
    assert dice2 != dice3
    assert dice3 != dice4

def test_save():
    dice1 = Dice(DiceValues.RAY)
    dice2 = Dice(DiceValues.HUMAN)
    dice3 = Dice(DiceValues.TANK)
    assert dice1.save() == 'Ray'
    assert dice2.save() == 'Human'
    assert dice3.save() == 'Tank'

def test_load():
    object1 = 'Ray'
    object2 = 'Human'
    object3 = 'Tank'
    dice1 = Dice.load(object1)
    dice2 = Dice.load(object2)
    dice3 = Dice.load(object3)
    assert dice1 == Dice(DiceValues.RAY)
    assert dice2 == Dice(DiceValues.HUMAN)
    assert dice3 == Dice(DiceValues.TANK)

def test_roll():
    dice = Dice(DiceValues.RAY)
    for i in range(1000):
        dice.roll()
        assert dice.value in DiceValues

def test_names():
    dice1 = Dice(DiceValues.RAY)
    dice2 = Dice(DiceValues.HUMAN)
    dice3 = Dice(DiceValues.TANK)
    assert dice1.name() == 'Ray'
    assert dice2.name() == 'Human'
    assert dice3.name() == 'Tank'
