from src.dice import Dice, DiceValues as DV
from src.player import Player
from src.game_state import GameState

data = {
    "player": 1,
    "remaining_dice": ['Ray', 'Human', 'Tank', 'Chicken', 'Tank', 'Cow', 'Ray'],
    "chosen_dice": ['Ray', 'Ray', 'Cow', 'Cow', 'Cow', 'Tank'],
    "players": [
    {
        "name": "Alex",
        "score": 7,
    },
    {
        "name": "Daniil",
        "score": 4,
    }
    ]
}

alex = Player.load(data["players"][0])
daniil = Player.load(data["players"][1])

players = [alex, daniil]
remaining_dice = ['Ray', 'Human', 'Tank', 'Chicken', 'Tank', 'Cow', 'Ray']
chosen_dice = ['Ray', 'Ray', 'Cow', 'Cow', 'Cow', 'Tank']

def test_init():
    game = GameState(players=players, remaining_dice=remaining_dice,
                     chosen_dice=chosen_dice, player=1)
    assert game.players == players
    assert game.remaining_dice == [Dice(DV.RAY), Dice(DV.HUMAN), Dice(DV.TANK), Dice(DV.CHICKEN),
                                   Dice(DV.TANK), Dice(DV.COW), Dice(DV.RAY)]
    assert game.chosen_dice == [Dice(DV.RAY), Dice(DV.RAY), Dice(DV.COW),
                                Dice(DV.COW), Dice(DV.COW), Dice(DV.TANK)]
    assert game.player == 1

def test_eq():
    game1 = GameState(players=players, remaining_dice=remaining_dice,
                     chosen_dice=chosen_dice, player=1)
    game2 = GameState(players=players, remaining_dice=data['remaining_dice'],
                     chosen_dice=data['chosen_dice'], player=data['player'])
    game3 = GameState(players=players, remaining_dice=remaining_dice,
                     chosen_dice=chosen_dice, player=2)
    assert game1 == game2
    assert game1 != game3

def test_save():
    game = GameState(players=players, remaining_dice=remaining_dice,
                     chosen_dice=chosen_dice, player=1)
    assert game.save() == data

def test_load():
    game = GameState.load(data)
    assert game.save() == data

def test_current_player():
    game1 = GameState.load(data)
    game2 = GameState.load(data)
    game2.player = 0
    assert game1.current_player() == daniil
    assert game2.current_player() == alex

def test_next_player():
    game = GameState.load(data)
    assert game.current_player() == daniil

    game.next_player()
    assert game.current_player() == alex
    game.next_player()
    assert game.current_player() == daniil

def test_prepare_new_dices():
    game = GameState.load(data)
    game.prepare_new_dices()
    assert len(game.remaining_dice) == 13
    assert len(game.chosen_dice) == 0

def test_choose_dice():
    game = GameState.load(data)
    game.choose_dice(Dice(DV.RAY))
    assert game.remaining_dice == [Dice(DV.HUMAN), Dice(DV.TANK), Dice(DV.CHICKEN), Dice(DV.TANK), Dice(DV.COW)]
    assert game.chosen_dice == [Dice(DV.RAY), Dice(DV.RAY), Dice(DV.COW), Dice(DV.COW),
                                Dice(DV.COW), Dice(DV.TANK), Dice(DV.RAY), Dice(DV.RAY)]

def test_add_score():
    game = GameState.load(data)
    assert game.add_score() == 3

    game.chosen_dice = [Dice(DV.HUMAN), Dice(DV.COW), Dice(DV.CHICKEN)]
    assert game.add_score() == 6

    game.chosen_dice.append(Dice(DV.TANK))
    assert game.add_score() == 0
