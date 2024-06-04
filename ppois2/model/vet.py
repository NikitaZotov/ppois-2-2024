import re

class Vet:
    def __init__(self):
        self.__fio = ''

    @classmethod
    def check_fio(cls, fio):
        if not re.match(r'^[А-Яа-яЁё\s]+$', fio):
            raise TypeError("Неправильно написано ФИО")
        parts = fio.split()
        if len(parts) != 3:
            raise TypeError("Неправильно написано ФИО")
        for part in parts:
            if len(part) < 2:
                raise TypeError("Неправильно написано ФИО")

        return True

    @property
    def fio(self):
        return self.__fio

    @fio.setter
    def fio(self, fio):
        self.check_fio(fio)
        self.__fio = fio

    def __str__(self):
        return (f'Name : {self.fio}')
