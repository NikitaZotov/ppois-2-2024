import xml.etree.ElementTree as ET
from Model.tournament import Tournament
from datetime import datetime


class Database:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

    def get_all_data(self):
        data = []
        for i in range(len(self.root)):
            data.append(Tournament(self.root[i][0].text,
                                   self.root[i][1].text,
                                   self.root[i][2].text,
                                   self.root[i][3].text,
                                   float(self.root[i][4].text),
                                   tournament_id=self.root[i].attrib['id']))
        return data

    def get_data(self, index: int) -> Tournament:
        data = Tournament(self.root[index][0].text,
                          self.root[index][1].text,
                          self.root[index][2].text,
                          self.root[index][3].text,
                          float(self.root[index][4].text),
                          tournament_id=self.root[index].attrib['id'])
        return data

    def get_all_name_sport(self) -> list[str]:
        sports = set()
        """for i in range(len(self.root)):
            sports.add(self.root[i][2].text)
        return sorted(list(sports))"""
        for sport_name in self.root.iter('sport_name'):
            sports.add(sport_name.text)
        return sorted(list(sports))

    def add_data(self, data: Tournament):
        new_data = ET.Element('tournament')
        new_data.set('id', str(len(self.root)+1))
        tournament_name = ET.SubElement(new_data, 'tournament_name')
        date_tournament = ET.SubElement(new_data, 'date')
        sport_name = ET.SubElement(new_data, 'sport_name')
        winners_name = ET.SubElement(new_data, 'winners_name')
        prize_money = ET.SubElement(new_data, 'prize_money')
        tournament_name.text = data.name_tournament
        date_tournament.text = data.date
        sport_name.text = data.name_sport
        winners_name.text = data.name_winner
        prize_money.text = str(data.prize_pool)
        self.root.append(new_data)
        self.save_data()

    def refactor_id(self):
        for i in range(len(self.root)):
            self.root[i].attrib['id'] = f"{i+1} "

    def search_data(self, search_type: int, first_search, second_search=0) -> list[Tournament]:
        search_result = []
        if second_search == 0:
            i = 0
            while i < len(self.root):
                if self.root[i][search_type].text == first_search:
                    search_result.append(self.get_data(i))
                i += 1
        else:
            coef = 1
            typer = 0
            if search_type == 5:
                coef = 0.6
                typer = 1
            i = 0
            while i < len(self.root):
                if first_search <= float(self.root[i][search_type-typer].text)*coef <= second_search:
                    search_result.append(self.get_data(i))
                i += 1
            print(len(search_result))
        return search_result

    def delete_data(self, type_delete: str or int, first_delete, second_delete=0) -> int:
        delete_list = {'tournament_name':  0, 'date': 1, 'sport_name': 2, 'winners_name': 3, 'prize_money': 4}

        delete_flag = 0
        if second_delete == 0:
            i = 0
            while i < len(self.root):
                if self.root[i][type_delete].text == first_delete:
                    self.root.remove(self.root[i])
                    delete_flag += 1
                else:
                    i += 1
        else:
            coef = 1
            typer = 0
            if type_delete == 5:
                coef = 0.6
                typer = 1
            i = 0
            while i < len(self.root):
                if (first_delete <= float(self.root[i][type_delete-typer].text)*coef <= second_delete):
                    self.root.remove(self.root[i])
                    delete_flag += 1
                else:
                    i += 1
        self.refactor_id()
        self.save_data()
        return delete_flag

    def save_data(self):
        self.tree.write(self.file_path)


if __name__ == '__main__':
    database = Database('tournaments.xml')
    tournament = Tournament("all", "2021-07-07", "dal", "sasd", 900)
    for i in range(8):
        database.add_data(tournament)
    alls = database.search_data(3, "cs go")
    print(len(alls))
    for i in alls:
        i.print_all()
