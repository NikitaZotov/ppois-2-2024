from typing import List
from lxml import etree


class Model:

    def __init__(self):
        self.persons: List[tuple] = []
        self.found_persons: List[tuple] = []
        self.current_page = 0
        self.items_per_page = 10

    def get_page(self):
        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page
        return self.persons[start_index:end_index]

    def get_total_pages(self):
        return (len(self.persons) + self.items_per_page - 1) // self.items_per_page

    def reset_page(self):
        self.current_page = 0

    def next_page(self):
        if self.current_page < self.get_total_pages() - 1:
            self.current_page += 1

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1

    def get_current_persons(self):
        return self.persons if not self.found_persons else [self.persons[i] for i in self.found_persons]

    def add_to_list(self, person: tuple):
        self.persons.append(person)

    def delete_from_list(self, person: tuple):
        self.persons.remove(person)

    def read_new_person(self):
        return self.persons[-1]

    def serialize_to_xml(self, filename):
        # Создаем корневой элемент
        root = etree.Element("Persons")

        # Добавляем элементы для каждой персоны
        for person in self.persons:
            person_elem = etree.SubElement(root, "Person")
            for i, attribute in enumerate(person):
                subelem = etree.SubElement(person_elem, f"Attribute{i + 1}")
                subelem.text = str(attribute)  # Приводим значения к строке

        # Записываем XML в файл
        with open(filename, 'wb') as file:  # wb - bin
            file.write(etree.tostring(root, pretty_print=True, encoding='utf-8'))  # pretty_print для лучшей читаемости
            #благодаря with файл автоматом закроется

    def deserialize_from_xml(self, filename):
        persons = []
        for event, elem in etree.iterparse(filename, events=('start', 'end')):
            if event == 'start' and elem.tag == 'Person':
                attributes = []
                for child in elem:
                    attributes.append(child.text)
                persons.append(tuple(attributes))
        self.persons = persons