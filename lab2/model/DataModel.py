from model.SearchModel import SearchModel
from model.player import Player
from model.team import Team
from abc import ABC


class DataModel(ABC):
    def get_players(self) -> list[Player]:
        pass

    def add_player(self, sport_name: str, name: str, cast: str, position: str, title: str, rank: str) -> None:
        pass

    def delete_players(self, search: SearchModel) -> int:
        pass

    def get_sports(self) -> list[Team]:
        pass

    def get_sport_by_name(self, name: str) -> Team:
        pass

    def search_players(self, search: SearchModel) -> list[Player]:
        pass

    def count_players_amount(self) -> int:
        pass

    def count_sports_amount(self) -> int:
        pass

    def add_sport(self, name: str, players_number: str) -> None:
        pass

    def player_exists(self, sport_name: str, name: str, cast: str, position: str, title: str, rank: str) -> bool:
        pass

    def sport_exists(self, name: str) -> bool:
        pass

    def creation(self) -> None:
        pass
