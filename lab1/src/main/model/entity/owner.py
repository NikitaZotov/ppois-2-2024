class Owner:
    def __init__(self, passport_id: str, first_name: str, last_name: str):
        self.__passport_id = passport_id
        self.__first_name = first_name
        self.__last_name = last_name

    @property
    def passport_id(self):
        return self.__passport_id

    @passport_id.setter
    def passport_id(self, passport_id: str):
        self.__passport_id = passport_id

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name: str):
        self.__first_name = first_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name: str):
        self.__last_name = last_name

    def __str__(self):
        return f"Owner[passport_id='{self.passport_id}', first_name='{self.first_name}', last_name='{self.last_name}']"

    def __eq__(self, other):
        if isinstance(other, Owner):
            return self.passport_id == other.passport_id
