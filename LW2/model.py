from typing import List
from lxml import etree


class Model:

    def __init__(self):
        self.persons: List[tuple] = []
        self.found_persons: List[tuple] = []

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


