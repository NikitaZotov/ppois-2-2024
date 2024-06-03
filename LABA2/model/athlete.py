import uuid


class Athlete:
    def __init__(self, sport_name: str, name: str, cast: str, position: str, title: int, rank: str, id: uuid.UUID):
        self.__sport_name = sport_name
        self.__name = name
        self.__cast = cast
        self.__position = position
        self.__title = title
        self.__rank = rank
        self.__id = id

    def get_sport_name(self):
        return self.__sport_name

    def get_name(self):
        return self.__name

    def get_cast(self):
        return self.__cast

    def get_position(self):
        return self.__position

    def get_title(self):
        return self.__title

    def get_rank(self):
        return self.__rank

    def get_id(self):
        return self.__id

    def tuple(self):
        values_tuple: tuple = (
            self.__sport_name,
            self.__name,
            self.__cast,
            self.__position,
            self.__title,
            self.__rank,
            self.__id.__str__()
        )
        return values_tuple

    def __str__(self):
        return (f"Sport Name: {self.__sport_name}, Name: {self.__name}, Cast: {self.__cast}, "
                f"Position: {self.__position}, Title: {self.__title}, Rank: {self.__title}, Id: {self.__id}")

