import uuid


class Sport:
    def __init__(self, name: str, athletes_number: int, id: uuid.UUID):
        self.__name = name
        self.__athletes_number = athletes_number
        self.__id = id

    def get_name(self):
        return self.__name

    def get_athletes_number(self):
        return self.__athletes_number

    def get_id(self):
        return self.__id

    def tuple(self):
        values_tuple: tuple = (
            self.__name,
            self.__athletes_number,
            self.__id.__str__(),
        )
        return values_tuple

    def __str__(self):
        return f"Name: {self.__name}, Athletes number: {self.__athletes_number}, Id: {self.__id}"
