from model.SearchModel import SearchModel
from model.athlete import Athlete
from model.sport import Sport
from abc import ABC


class DataModel(ABC):
    def get_athletes(self) -> list[Athlete]:
        pass

    def add_athlete(self, sport_name: str, name: str, cast: str, position: str, title: str, rank: str) -> None:
        pass

    def delete_athletes(self, search: SearchModel) -> int:
        pass

    def get_sports(self) -> list[Sport]:
        pass

    def get_sport_by_name(self, name: str) -> Sport:
        pass

    def search_athletes(self, search: SearchModel) -> list[Athlete]:
        pass

    def count_athletes_amount(self) -> int:
        pass

    def count_sports_amount(self) -> int:
        pass

    def add_sport(self, name: str, athletes_number: str) -> None:
        pass

    def athlete_exists(self, sport_name: str, name: str, cast: str, position: str, title: str, rank: str) -> bool:
        pass

    def sport_exists(self, name: str) -> bool:
        pass

    def creation(self) -> None:
        pass
