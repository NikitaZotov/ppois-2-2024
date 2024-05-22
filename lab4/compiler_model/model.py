import pickle
from person import Programmer
from programming_language import ProgrammingLanguage
class Model:
    def __init__(self):
        self.programmer = Programmer()
        self.programming_language = ProgrammingLanguage()

    def load_info_person(self):
        try:
            with open("personal_data", "rb") as file:
                self.programmer = pickle.load(file)
            return True
        except FileNotFoundError:
            return False

    def load_info_language(self):
        try:
            with open("programming_language", "rb") as file:
                self.programming_language = pickle.load(file)
            return True
        except FileNotFoundError:
            return False

    def set_new_person_data(self,fio,age,exp):
        self.programmer.full_name = fio
        self.programmer.age = age
        self.programmer.experience = exp

    def safe_person_data(self):
        with open("personal_data", "wb") as file:
            pickle.dump(self.programmer, file)

    def safe_language_data(self):
        with open("programming_language", "wb") as file:
            pickle.dump(self.programming_language, file)

    def get_info_about_language(self):
        if self.programming_language.name == "" or self.programming_language.file_extension == "":
            return f"Ошибка найстроки параметров языка\n", False
        if self.programmer.full_name == "" or self.programmer.age == "":
            return f"Пользователь не был найден\n", False
        return f"Настройки языка и пользователя удовлетворяют для начала компиляции\n", True

    def add_lang_name(self,name):
        self.programming_language.name = name

    def add_lang_ext(self,ext):
        self.programming_language.file_extension = ext