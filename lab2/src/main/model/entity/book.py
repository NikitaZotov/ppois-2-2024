from dataclasses import dataclass


@dataclass
class Book:

    title: str
    author_fio: str
    publisher: str
    volumes_num: int = 0
    circulation: int = 0
    total_volumes: int = 0

    def __iter__(self):
        return iter(self.__dict__.items())