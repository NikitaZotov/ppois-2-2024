import shelve


class ShelveSerializer:

    def __init__(self, save_file_path: str = "cad_agency/model/serialize/files/db"):
        self.__save_file_path = save_file_path

    @property
    def save_file_path(self) -> str:
        return self.__save_file_path

    @save_file_path.setter
    def save_file_path(self, save_file_path: str):
        self.__save_file_path = save_file_path

    def serialize(self, **kwargs):
        with shelve.open(self.__save_file_path) as shelf:
            shelf.update(**kwargs)

    def deserialize(self) -> dict:
        with shelve.open(self.__save_file_path) as shelf:
            return dict((i, shelf[i]) for i in shelf.keys())
