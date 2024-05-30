import xml.etree.ElementTree as ET


class Table:
    def __init__(self, file_path="D:/lab1/ppois3/Model/record.xml"):
        self.file_path = file_path
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

    def get_first(self):
        return [self.root[0][0].text, int(self.root[0][1].text)]

    def get_five_first(self):
        result = []
        for i in range(0, min(len(self.root), 5)):
            record = [self.root[i][0].text, int(self.root[i][1].text)]
            result.append(record)
        return result

    def add_record(self, record: list[str | int]):
        new_record = ET.Element('record')
        name_player = ET.SubElement(new_record, 'name_player')
        goals_number = ET.SubElement(new_record, 'goals_number')
        name_player.text = record[0]
        goals_number.text = str(record[1])
        self.root.append(new_record)
        self.sorting()

    def sorting(self):
        # Получаем все записи в виде списка
        records = list(self.root)

        # Сортируем записи по полю 'goals_number' в порядке убывания
        records.sort(key=lambda x: int(x.find('goals_number').text),reverse=True)

        # Очищаем корневой элемент
        while len(self.root)>0:
            self.root.remove(self.root[-1])

        # Добавляем отсортированные записи обратно в корневой элемент
        for record in records:
            self.root.append(record)

        # Сохраняем изменения в файл
        self.tree.write(self.file_path)

    def cout_all(self):
        for record in self.root:
            print(f"name:{record[0].text} goals_number:{record[1].text}")


if __name__ == '__main__':
    table = Table()
    table.cout_all()
    table.sorting()
    table.cout_all()
    table.add_record(["Tsar2", 8])
    table.add_record(["Tsar1", 1])
    table.add_record(["Tsar0", 0])
    print(table.get_first())
    print(table.get_five_first())



