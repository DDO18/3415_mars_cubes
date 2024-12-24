import json
from pathlib import Path

from src.dice import Dice, DiceValues as DV
from src.player import Player
from src.game_state import GameState
from src.player_interaction import PlayerInteraction
import src.player_interactions as all_player_types
import enum


class GamePhase(enum.StrEnum):
    NEW_ROUND = "New round"
    CHOOSE_DICE = "Choose dice"
    ADD_SCORE = "Add score"
    NEXT_PLAYER = "Switch current player"
    DECLARE_WINNER = "Declare a winner"
    GAME_END = "Game ended"

class GameServer:
    def __init__(self, player_types, game_state):
        self.player_types = player_types
        self.game_state = game_state

    @classmethod
    def load_game(cls, filename: str | Path):
        with open(filename, 'r') as file_in:
            data = json.load(file_in)
            game_state = GameState.load(data)
            player_types = {}
            for player, player_data in zip(game_state.players, data['players']):
                kind = player_data['kind']
                kind = getattr(all_player_types, kind)
                player_types[player] = kind
            return GameServer(player_types = player_types, game_state = game_state)

    def save_to_dict(self):
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            data['players'][player_index]['kind'] = self.player_types[player].__name__
        return data

    def save(self, filename: str | Path):
        data = self.save_to_dict()
        with open(filename, 'w') as file_out:
            json.dump(data, file_out, indent=4)

    @staticmethod
    def request_player_count() -> int:
        while True:
            try:
                player_count = int(input("Сколько марсиан играет? "))
                if 2 <= player_count <= 10:
                    return player_count
            except ValueError:
                pass
            print("Введите кол-во игроков от 2 до 10")

    @staticmethod
    def request_player() -> (str, PlayerInteraction):
        while True:
            name = input("Как зовут марсианина? ")
            if name.isalpha():
                break
            print("Имя игрока должно содержать только буквы")
        while True:
            try:
                kind = input("Какой это игрок?: ")
                kind = getattr(all_player_types, kind)
                break
            except AttributeError:
                print("Виды игроков: Bot, Martian")
        return name, kind

    @classmethod
    def new_game(cls):
        player_count = cls.request_player_count()
        player_types = {}
        for p in range(player_count):
            name, kind = cls.request_player()
            player = Player(name = name, score = 0)
            player_types[player] = kind
        game_state = GameState(list(player_types.keys()))
        return cls(player_types, game_state)

    def run(self):
        current_phase = GamePhase.NEW_ROUND
        while current_phase != GamePhase.GAME_END:
            phases = {
                GamePhase.NEW_ROUND: self.new_round,
                GamePhase.CHOOSE_DICE: self.choose_dice_phase,
                GamePhase.ADD_SCORE: self.add_score_phase,
                GamePhase.NEXT_PLAYER: self.next_player,
                GamePhase.DECLARE_WINNER: self.declare_winner,
            }
            current_phase = phases[current_phase]()
        print("Игра завершена")

    def new_round(self) -> GamePhase:
        self.game_state.prepare_new_dices()
        print('Новый раунд')
        print('Текущие очки игроков:')
        for player in self.game_state.players:
            print(f"{player.name}: {player.score}")
        for player in self.game_state.players:
            if player.score >= 25: return GamePhase.DECLARE_WINNER
        return GamePhase.CHOOSE_DICE

    def choose_dice_phase(self) -> GamePhase:
        print(f'Фаза выбора кубика, ход {self.game_state.current_player().name}')
        print(f'Доступные кубики: {self.game_state.remaining_dice}')
        current_player = self.game_state.current_player()
        interaction = self.player_types[current_player]
        flag = False
        for dice in self.game_state.remaining_dice:
            flag = self.game_state.can_choose_dice(dice)
            if flag:
                break
        if not flag:
            return GamePhase.ADD_SCORE
        while True:
            try:
                choice_dice = interaction.choose_dice(self.game_state.remaining_dice)
                self.game_state.choose_dice(choice_dice)
                if Dice(DV.TANK) in self.game_state.remaining_dice:
                    self.game_state.choose_dice(DV.TANK)
                self.game_state.reroll()
                return GamePhase.CHOOSE_DICE
            except (AssertionError, ValueError):
                continue

    def add_score_phase(self) -> GamePhase:
        self.game_state.current_player().score += self.game_state.add_score()
        return GamePhase.NEXT_PLAYER

    def next_player(self) -> GamePhase:
        self.game_state.prepare_new_dices()
        previous_player = self.game_state.player
        self.game_state.next_player()
        current_player = self.game_state.player
        if previous_player != 0 and current_player == 0:
            return GamePhase.NEW_ROUND
        else:
            return GamePhase.CHOOSE_DICE

    def declare_winner(self) -> GamePhase:
        max_score = max([player.score for player in self.player_types])
        for player in self.game_state.players:
            if player.score == max_score: print(f"{player.name} победитель!")
        return GamePhase.GAME_END

def __main__():
    load = False
    if load:
        server = GameServer.load_game('mars.json')
    else:
        server = GameServer.new_game()
    server.run()

if __name__ == "__main__":
    __main__()
