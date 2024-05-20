from model.FileModel import FileModel
from model.DbModel import DbModel
from model.sport import Sport
from model.athlete import Athlete
from model.SearchModel import SearchModel


class DataPresenter:
    def __init__(self):
        self.__model = None

    def select_model(self, file_name: str) -> None:
        if file_name is not None and len(file_name) > 0:
            if file_name.endswith('.db'):
                self.close_data_source()
                self.__model = DbModel(file_name)
            elif file_name.endswith('.xml'):
                self.close_data_source()
                self.__model = FileModel(file_name)

    def get_model(self):
        return self.__model

    def creation(self) -> None:
        self.__model.creation()

    def close_data_source(self):
        self.__model = None

    def add_sport(self, name: str, athletes_number: str) -> None:
        self.__model.add_sport(name, athletes_number)
        return None

    def sport_exists(self, name: str) -> bool:
        return self.__model.sport_exists(name)

    def get_sports(self, start='', end='') -> list[Sport]:
        if start == '':
            return self.__model.get_sports()
        return self.__model.get_sports()[start:end]

    def get_sport_by_name(self, name: str) -> Sport:
        return self.__model.get_sport_by_name(name)

    def count_sports_amount(self) -> int:
        return self.__model.count_sports_amount()

    def add_athlete(self, sport_name: str, name: str, cast: str, position: str, title: str, rank: str) -> None:
        self.__model.add_athlete(sport_name, name, cast, position, title, rank)
        return None

    def athlete_exists(self, sport_name: str, name: str, cast: str, position: str, title: str, rank: str) -> bool:
        return self.__model.athlete_exists(sport_name, name, cast, position, title, rank)

    def delete_athletes(self, search: SearchModel) -> int:
        return self.__model.delete_athletes(search)

    def get_athletes(self, start, end) -> list[Athlete]:
        return self.__model.get_athletes()[start:end]

    def search_athletes(self, search: SearchModel) -> list[Athlete] | None:
        return self.__model.search_athletes(search)

    def count_athletes_amount(self) -> int:
        return self.__model.count_athletes_amount()
