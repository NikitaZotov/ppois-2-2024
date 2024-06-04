from model.FileModel import FileModel
from model.team import Team
from model.player import Player
from model.SearchModel import SearchModel


class DataController:
    def __init__(self):
        self.__model = None

    def select_model(self, file_name: str) -> None:
        if file_name is not None and len(file_name) > 0:
            self.close_data_source()
            self.__model = FileModel(file_name)

    def get_model(self):
        return self.__model

    def creation(self) -> None:
        self.__model.creation()

    def close_data_source(self):
        self.__model = None

    def add_sport(self, name: str, players_number: str) -> None:
        self.__model.add_sport(name, players_number)
        return None

    def sport_exists(self, name: str) -> bool:
        return self.__model.sport_exists(name)

    def get_sports(self, start='', end='') -> list[Team]:
        if start == '':
            return self.__model.get_sports()
        return self.__model.get_sports()[start:end]

    def get_sport_by_name(self, name: str) -> Team:
        return self.__model.get_sport_by_name(name)

    def count_sports_amount(self) -> int:
        return self.__model.count_sports_amount()

    def add_player(self, sport_name: str, name: str, cast: str, position: str, title: str, rank: str) -> None:
        self.__model.add_player(sport_name, name, cast, position, title, rank)
        return None

    def player_exists(self, sport_name: str, name: str, cast: str, position: str, title: str, rank: str) -> bool:
        return self.__model.player_exists(sport_name, name, cast, position, title, rank)

    def delete_players(self, search: SearchModel) -> int:
        return self.__model.delete_players(search)

    def get_players(self, start, end) -> list[Player]:
        return self.__model.get_players()[start:end]

    def search_players(self, search: SearchModel) -> list[Player] | None:
        return self.__model.search_players(search)

    def count_players_amount(self) -> int:
        return self.__model.count_players_amount()
