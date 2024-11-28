import hashlib

class Player:

    def __init__(self, name: str, score: int):
        self.name = name
        self.score = score
        self.dices = ...
        self.chosen = ...

    def __str__(self):
        return f'Игрок: {self.name}, Очки: {self.score}'

    def  __eq__(self, other):
        return self.name == other.name and self.score == other.score

    def __hash__(self):
        return int(hashlib.sha1(self.name.encode("utf-8")).hexdigest(), 16) % (10**8)

    def save(self):
        return \
        {
            'name': self.name,
            'score': self.score
        }

    @staticmethod
    def load(data):
        return Player(name = data['name'], score = data['score'])
