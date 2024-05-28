from models.Director import Director
from models.Studio import Studio
from models.FilmSet import FilmSet
from models.Script import Script
from models.Actor import Actor


def create_studio(studio_name, studio_number, old_number, young_number):
    if (old_number + young_number == studio_number):
        studio = Studio(studio_name, studio_number)
        studio.set_young_old_numbers(young_number, old_number)
        return studio
    else:
        raise ValueError("Кол-во актеров не совпадает.")
        


def create_filmset(filmset_type):
    film_set = FilmSet(filmset_type)
    return film_set


def create_script(script_name, script_type, script_person_number, script_plot, script_experience, film_set, studio):
    script = Script(script_name, script_type, script_person_number, script_plot, script_experience)
    if script_type != film_set.get_film_set_type():
        raise ValueError("Тип сценария должен совпадать с типо площадки")
    if script_person_number != studio.get_person_number():
        raise ValueError("Кол-во актеров должно совпадать с кол-вом актеров студии")
    return script


def create_director(director_name, director_exp, script):
    director = Director(director_name)
    director.change_experience(director_exp, script)
    if director.get_experience() < script.get_experience_director():
        raise ValueError("Опыт режиссера меньше необходимого для данного сценария.")
    director.change_experience(director_exp, script)
    return director



def create_actors(studio, actor_name, actor_age):
    if studio.compare_numbers_people():
        actor = Actor(actor_name, actor_age)
        if len(studio.get_list_old_persons()) + len(studio.get_list_young_persons()) < studio.get_person_number():
           return studio.add_person(actor)
        else:
            raise ValueError("Актеров слишком много.")
    else:
        raise ValueError("Невозможно добавить актера. Некорректное количество людей в студии.")




def create_shots(camera, montage, direction):
    if direction == "r":
        return camera.turn_right(montage)
    elif direction == "l":
        return camera.turn_left(montage)
    elif direction == "u":
        return camera.turn_up(montage)
    elif direction == "d":
        return camera.turn_down(montage)
    else:
        raise ValueError("Некорректное расположение.")


def make_post_production(post_production, montage, action, pos1, pos2=None):
    if action == "del":
        return post_production.del_shot(pos1, montage)
    elif action == "ch":
        if pos2 is None:
            raise ValueError("Для изменения позиции кадра требуется новая позиция.")
        return post_production.change_shot_place(pos2, pos1, montage)
    else:
        raise ValueError("Некорректное действие.")
        

def make_realization(post_production, studio, script, director, montage):
    post_production.make_realization(studio, script, director, montage)


def change_number_actors(studio, number, script, old_number, young_number):
    studio.set_number_people(number, script, old_number, young_number)
