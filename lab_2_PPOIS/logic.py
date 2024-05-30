# -*- coding: utf-8 -*-
import datetime as dt
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog as fd

list_of_players = []

def get_players(page_num):
    list_ = []
    for i in range((page_num-1)*10, min(page_num*10, len(list_of_players))):
        list_.append([list_of_players[i].last_name + ' ' + list_of_players[i].first_name + ' ' +
                      list_of_players[i].middle_name, list_of_players[i].date_of_birth,
                      list_of_players[i].football_team, list_of_players[i].birth_town,
                      list_of_players[i].sostav, list_of_players[i].position])
    return list_


class Football_player:
    def __init__(self, first_name, middle_name, last_name, date_of_birth, football_team, birth_town, sostav, position):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.football_team = football_team
        self.birth_town = birth_town
        self.sostav = sostav
        self.position = position

def save_file():
    filepath = fd.asksaveasfilename()
    if filepath != "":
        create_xml(filepath)

def read_file():
    filepath = fd.askopenfilename()
    if filepath != "":
        read_xml(filepath)

def add_to_list(name, mname, lname, bdate, team, town, sost, pos):
    list_of_players.append(Football_player(name,mname,lname, bdate,team,town,sost,pos))

def find_players(name, mname, lname, bdate, team, town, sost, pos):
    search_result = list_of_players.copy()
    if(name != ''):
        for element in search_result:
            if(element.first_name != name):
                search_result.remove(element)
    if (mname != ''):
        for element in search_result:
            if (element.middle_name != mname):
                search_result.remove(element)
    if (lname != ''):
        for element in search_result:
            if (element.last_name != lname):
                search_result.remove(element)
    if (bdate != ''):
        for element in search_result:
            if (element.date_of_birth != bdate):
                search_result.remove(element)
    if (town != ''):
        for element in search_result:
            if (element.birth_town != town):
                search_result.remove(element)
    if (team != ''):
        for element in search_result:
            if (element.football_team != team):
                search_result.remove(element)
    if (sost != ''):
        for element in search_result:
            if (element.sostav != sost):
                search_result.remove(element)
    if (pos != ''):
        for element in search_result:
            if (element.position != pos):
                search_result.remove(element)
    search_result_print = []
    for element in search_result:
        search_result_print.append([element.last_name + ' ' + element.first_name + ' ' +
                      element.middle_name, element.date_of_birth,
                      element.football_team, element.birth_town,
                      element.sostav, element.position])
    return search_result_print, search_result

def delete_info(list_of_players_del):
    for element in list_of_players_del:
        list_of_players.remove(element)
def create_xml(file_name):
    file = 'players.xml'
    data_xml = ET.Element("players")
    data_xml.append(ET.Element("player"))
    data = ET.ElementTree(data_xml)
    b_xml = ET.tostring(data_xml)

    # Opening a file under the name `items2.xml`,
    # with operation mode `wb` (write + binary)
    with open("GFG.xml", "wb") as f:
        f.write(b_xml)
    #myfile = open(file, 'wb')
    #data.write(myfile)
    for player in list_of_players:
        football_player = ET.SubElement(data_xml, 'Player')
        player_fname = ET.SubElement(football_player, 'first name')
        player_fname.text = player.first_name
        player_mname = ET.SubElement(football_player, 'middle name')
        player_mname.text = player.middle_name
        player_lname = ET.SubElement(football_player, 'last name')
        player_lname.text = player.last_name
        player_bdate = ET.SubElement(football_player, 'date of birth')
        player_bdate.text = player.date_of_birth
        player_team = ET.SubElement(football_player, 'football team')
        player_team.text = player.football_team
        player_town = ET.SubElement(football_player, 'birth town')
        player_town.text = player.birth_town
        player_sostav = ET.SubElement(football_player, 'sostav')
        player_sostav.text = player.sostav
        player_pos = ET.SubElement(football_player, 'position')
        player_pos.text = player.position
    data = ET.ElementTree(data_xml)
    myfile = open(file, "wb")
    data.write(myfile, encoding='utf-8', xml_declaration=True)

def read_xml(file_name):
    tree = ET.parse(file_name)
    list_of_players.clear()
    data_xml = tree.getroot()
    for elem in data_xml:
        player = []
        for subelem in elem:
            player.append(subelem.text)
        add_to_list(Football_player(player[0],player[1],player[2],player[3], player[4],
                                               player[5], player[6], player[7]))



#list_of_players.append(Football_player('1','2','3','4','5','6','7','8'))
#create_xml(list_of_players)