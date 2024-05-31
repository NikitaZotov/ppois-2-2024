# This is a sample Python script.
from random import choice
import datetime as dt
import logic as lg

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

pos_list = ['форвард', 'оттянутый нападающий', 'крайний нападающий', 'полусредний нападающий',
                'центральный опорный полузащитник', 'центральный полузащитник',
                'центральный атакующий полузащитник', 'фланговый полузащитник', 'центральный защитник',
                'свободный защитник(либеро)', 'фланговый защитник', 'вратарь']
sos_var = ['основной', 'запасной']
name_list = []
sname_list = []
lname_list = []
#data_list = []
#club_list = []
#city_list = []

name = open('names.txt', 'r',encoding='utf-8')
names = name.readlines()
for element in names:
    buf = element.split(' ')
    lname_list.append(buf[0])
    name_list.append(buf[1])
    sname_list.append(buf[2])
date_ = open('dates.txt', 'r', encoding='utf-8')
data_list = date_.readlines()
club1 = open('clubs_1.txt', encoding='utf-8')
club2 = open('clubs2.txt', encoding='utf-8')
club_list = club1.readlines() + club2.readlines()
city = open('cities.txt', encoding='utf-8')
city_list = city.readlines()

data_1 = []
data_2 = []
data_3 = []
data_4 = []



for i in range(0, 60):
    data_1.append( lg.Football_player(choice(name_list), choice(sname_list), choice(lname_list), dt.datetime.strptime(choice(data_list).strip(),'%d-%m-%Y'),
                                choice(club_list), choice(city_list), choice(sos_var), choice(pos_list)))
    data_2.append(lg.Football_player(choice(name_list), choice(sname_list), choice(lname_list), dt.datetime.strptime(choice(data_list).strip(),'%d-%m-%Y'),
                                     choice(club_list), choice(city_list), choice(sos_var), choice(pos_list)))
    data_3.append(lg.Football_player(choice(name_list), choice(sname_list), choice(lname_list), dt.datetime.strptime(choice(data_list).strip(),'%d-%m-%Y'),
                                     choice(club_list), choice(city_list), choice(sos_var), choice(pos_list)))
    data_4.append(lg.Football_player(choice(name_list), choice(sname_list), choice(lname_list), dt.datetime.strptime(choice(data_list).strip(),'%d-%m-%Y'),
                                     choice(club_list), choice(city_list), choice(sos_var), choice(pos_list)))

lg.list_of_players = data_1
lg.save_file()
lg.list_of_players = data_2
lg.save_file()
lg.list_of_players = data_3
lg.save_file()
lg.list_of_players = data_4
lg.save_file()


# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
