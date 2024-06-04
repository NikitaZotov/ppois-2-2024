import uuid


class Team:
    def __init__(self, name: str, players_number: int, id: uuid.UUID):
        self.__name = name
        self.__players_number = players_number
        self.__id = id

    def get_name(self):
        return self.__name

    def get_players_number(self):
        return self.__players_number

    def get_id(self):
        return self.__id

    def tuple(self):
        values_tuple: tuple = (
            self.__name,
            self.__players_number,
            self.__id.__str__(),
        )
        return values_tuple

    def __str__(self):
        return f"Name: {self.__name}, Players number: {self.__players_number}, Id: {self.__id}"
