from src.player import Player

alex_data = \
    {
        "name": "Alex",
        "score": 0
    }

def test_init():
    p = Player("Daniil", 4)
    assert p.name == "Daniil"
    assert p.score == 4

def test_str():
    p = Player("Daniil", 4)
    assert str(p) == 'Игрок: Daniil, Очки: 4'

def test_eq():
    p1 = Player("Daniil", 4)
    p2 = Player("Daniil", 4)
    assert p1 == p2

def test_save():
    p = Player("Alex", 0)
    assert p.save() == alex_data

def test_load():
    p = Player("Alex", 0)
    p_from_data = Player.load(alex_data)
    assert p == p_from_data
