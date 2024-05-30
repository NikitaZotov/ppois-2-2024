from Model.database import Database
from Model.tournament import Tournament


class MainController:
    def __init__(self, database: Database):
        self.database = database

    def get_all_tournaments(self):
        return self.database.get_all_data()

    def add_data(self, data: Tournament):
        self.database.add_data(data)
        return True

    def delete_data(self, delete_type: int, first_elem, second_elem: float = 0):
        score_delete = self.database.delete_data(delete_type, first_elem, second_delete=second_elem)
        return score_delete

    def search_data(self, search_type: int, first_elem, second_elem: float = 0):
        result_list = []
        result_list = self.database.search_data(search_type, first_elem, second_search=second_elem)
        return result_list
    def get_sports(self):
        return self.database.get_all_name_sport()