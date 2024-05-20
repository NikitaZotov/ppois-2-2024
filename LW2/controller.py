from tkinter import filedialog
import re
from model import Model


class Controller:
    def __init__(self, model: Model):
        self.model = model
        self.view = None

    def setView(self, view):
        self.view = view  # Устанавливаем представление для контроллера

    def add_to_model(self, person: tuple):
        try:
            person_list = list(person)
            last_element_index = len(person_list) - 1
            try:
                person_list[last_element_index] = int(person_list[last_element_index])
            except ValueError:
                raise ValueError("Введено нечисловое значение для стажа!")
            if person_list[last_element_index] < 0:
                raise ValueError("Стаж работы имеет отрицательное значение!")
            if person_list[last_element_index] > 50:
                raise ValueError("Стаж работы имеет слишком большое значение!")  # написать проверку на ввод нечислового
            person = tuple(person_list)
            self.model.add_to_list(person)
        except ValueError as e:
            raise ValueError(e)

    def delete_person_by_conditions(self, conditions):
        try:
            # Проверяем, были ли использованы какие-либо условия
            if not conditions:
                raise ValueError("Нет совпадений для удаления")

            persons_to_delete = [index for index, person in enumerate(self.model.persons)
                                 if all(condition(person) for condition in conditions)]

            for index in sorted(persons_to_delete, reverse=True):
                del self.model.persons[index]
            self.view.update_table()
        except ValueError as e:
            self.view.show_error(str(e))

    def serialize(self):
        file = filedialog.asksaveasfile(defaultextension=".xml", initialdir="/",
                                        title="Выберите файл для сохранения")
        if file:  # Проверяем, что пользователь выбрал файл
            self.model.serialize_to_xml(
                file.name)  # file.name содержит полный путь к файлу, включая имя файла и расширение

    def deserialize(self):
        file_path = filedialog.askopenfilename(defaultextension=".xml", initialdir="D:\PPOIS\PPOIS4SEM\TKINTERGUIDE",
                                               title="Выберите файл для загрузки")
        if file_path:  # Проверяем, что пользователь выбрал файл
            self.model.deserialize_from_xml(file_path)  # Загружаем данные из выбранного файла

    def find_persons_by_conditions(self, conditions):
        try:
            if not conditions:
                raise ValueError("Не заданы условия поиска")

            self.view.model.found_persons = [index for index, person in enumerate(self.model.persons)
                                             if all(condition(person) for condition in conditions)]

            return self.view.model.found_persons
        except ValueError as e:
            self.view.show_error(str(e))

    def reset_search(self):
        self.view.model.found_persons = []
