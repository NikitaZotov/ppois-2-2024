import re


class Pet:
    def __init__(self):
        self.__name = ''
        self.__birth_date = ''
        self.__last_visit_date = ''
        self.__diagnosis = ''

    @classmethod
    def check_name(cls, name):
        if not re.match(r'^[А-Яа-яЁё\s]+$', name):
            raise TypeError("Неправильно написано имя")
        words = name.split()
        for word in words:
            if len(word) < 2:
                raise TypeError("Неправильно написано имя")
        return True

    @classmethod
    def check_date(cls, date):
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', date):
            raise TypeError("Неправильно написана дата")
        day, month, year = map(int, date.split('.'))
        if not (1 <= day <= 31):
            raise TypeError("Неправильно написана дата")
        if not (1 <= month <= 12):
            raise TypeError("Неправильно написана дата")
        if not (1900 <= year <= 2024):
            raise TypeError("Неправильно написана дата")

    @classmethod
    def check_diagnosis(cls, diagnosis):
        if re.match(r'^[А-Яа-яЁё0-9\s]+$', diagnosis):
            return True
        raise TypeError("Неправильно написан диагноз")

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.check_name(name)
        self.__name = name

    def get_birth_date(self):
        return self.__birth_date

    def set_birth_date(self, birth_date):
        self.check_date(birth_date)
        self.__birth_date = birth_date

    def get_last_visit_date(self):
        return self.__last_visit_date

    def set_last_visit_date(self, last_visit_date):
        self.check_date(last_visit_date)
        self.__last_visit_date = last_visit_date

    def get_diagnosis(self):
        return self.__diagnosis

    def set_diagnosis(self, diagnosis):
        self.check_diagnosis(diagnosis)
        self.__diagnosis = diagnosis

    name = property(get_name, set_name)
    birth_date = property(get_birth_date, set_birth_date)
    last_visit_date = property(get_last_visit_date, set_last_visit_date)
    diagnosis = property(get_diagnosis, set_diagnosis)

    def __str__(self):
        return (f'Name : {self.name}, Birth date : {self.birth_date}, '
                f'Last visit date: {self.last_visit_date}, Diagnosis : {self.diagnosis}')
