import uuid


class Player:
    def __init__(self, sport_name: str, name: str, cast: str, position: str, hometown: int, birthday: str, id: uuid.UUID):
        self.__name = name
        self.__sport_name = sport_name
        self.__cast = cast
        self.__position = position
        self.__hometown = hometown
        self.__birthday = birthday
        self.__id = id

    def get_name(self):
        return self.__name
    def get_sport_name(self):
        return self.__sport_name

    def get_cast(self):
        return self.__cast

    def get_position(self):
        return self.__position

    def get_hometown(self):
        return self.__hometown

    def get_birthday(self):
        return self.__birthday

    def get_id(self):
        return self.__id

    def tuple(self):
        values_tuple: tuple = (
            self.__name,
            self.__sport_name,
            self.__cast,
            self.__position,
            self.__hometown,
            self.__birthday,
            self.__id.__str__()
        )
        return values_tuple

    def __str__(self):
        return (f"Team Name: {self.__sport_name}, Name: {self.__name}, Cast: {self.__cast}, "
                f"Position: {self.__position}, Hometown: {self.__hometown}, Birthday: {self.__birthday}, Id: {self.__id}")

