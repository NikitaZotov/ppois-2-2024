import math
from models.sportsman import Sportsman

sportsman_list = []
rec_per_pag = 10
current_page = 1
total_pages = 1

def add_sportsman(full_name, team, position, titles, sport_type, rank):
    new_sportsman = Sportsman(full_name, team, position, titles, sport_type, rank)
    sportsman_list.append(new_sportsman)

def delete_sportsman(indices):
    global sportsman_list
    for index in reversed(indices):
        if index < len(sportsman_list):
            del sportsman_list[index]

def search_sportsmen(search_type, query):
    if search_type == "ФИО или Вид спорта":
        return [s for s in sportsman_list if query.lower() in s.full_name.lower() or query.lower() in s.sport_type.lower()]
    elif search_type == "Количество титулов":
        try:
            query = int(query)
            return [s for s in sportsman_list if s.titles == query]
        except ValueError:
            return []
    elif search_type == "ФИО или Разряд":
        return [s for s in sportsman_list if query.lower() in s.full_name.lower() or query.lower() in s.rank.lower()]
    return []

def get_total_pages():
    global total_pages
    total_pages = math.ceil(len(sportsman_list) / rec_per_pag)
    return total_pages

def get_sportsmen_for_page(page):
    global current_page
    current_page = page
    start_index = (current_page - 1) * rec_per_pag
    end_index = current_page * rec_per_pag
    return sportsman_list[start_index:end_index]
