from space_object import SpaceObject
from star import Star
from cometa import Cometa
from planet import Planet
from satellite import Satellite
from asteroid import Asteroid
import os
from spacecraft import Spacecraft
from star_system import StarSystem
import pickle


def search_planet(star_system=None) -> Planet:
    name = input("enter name planet")
    while True:
        try:
            speed = float(input("enter planet's speed"))
            break
        except ValueError:
            print("not a valid speed")
    while True:
        try:
            mass = float(input("enter planet mass"))
            break
        except ValueError:
            print("not a valid mass")
    while True:
        try:
            x = float(input("enter x planet position"))
            y = float(input("enter y planet position"))
            z = float(input("enter z planet position"))
            break
        except ValueError:
            print("not a valid coordinates")
    while True:
        try:
            radius = float(input("enter planet radius"))
            break
        except ValueError:
            print("not a valid radius")
    planet = Planet(name, speed, mass, x, y, z, radius)
    if star_system is not None:
        star_system.add_planet(planet)
    else:
        return planet


def create_system() -> StarSystem:
    print("create star")
    name = input("enter name star")
    type_star = input("enter star type")
    while True:
        try:
            speed = float(input("enter star speed"))
            break
        except ValueError:
            print("not a valid speed")
    while True:
        try:
            mass = float(input("enter star mass"))
            break
        except ValueError:
            print("not a valid mass")
    while True:
        try:
            radius = float(input("enter star radius"))
            break
        except ValueError:
            print("not a valid radius")
    star = Star(name, type_star, speed, mass, 0, 0, 0, radius)
    planet = search_planet()
    print(planet.get_z())
    star_system = StarSystem(star=star, planets=[planet])
    return star_system


def launch_spacecraft(star_system):
    while True:
        try:
            planet_name = input("enter planet's name with spacelaunch")
            planet = star_system.search_planet(planet_name)
            break
        except ValueError:
            print("not a found planet. Try again")
    spacecraft_name = input("enter spacecraft name")
    star_system.add_spacecraft(planet.start_spacecraft(spacecraft_name))


def analysis_spaceobject(star_system):
    spaceobject = None
    while True:
        try:
            spaceobject_name = input("enter spaceobject's name\t")
            spaceobject = star_system.search_space_object(spaceobject_name)
            break
        except ValueError:
            print("not a found spaceobject. Try again")
    try:
        spacecraft_name = input("enter spacecraft name")
        spacecraft = star_system.search_spacecraft(spacecraft_name)
    except ValueError:
        print("not a found spacecraft.")
        return

    print(type(spaceobject))
    spacecraft.analysis_space_object(spaceobject)


def analysis_planet(star_system):
    while True:
        try:
            planet_name = input("enter planet's name")
            planet = star_system.search_space_object(planet_name)
            break
        except ValueError:
            print("this planet not exist. Try again")
    try:
        spacecraft_name = input("enter spacecraft's name for analysis")
        spacecraft = star_system.search_spacecraft(spacecraft_name)
    except ValueError:
        print("this spacecraft not exist.Try again")
        return
    spacecraft.analysis_planet(planet)


def search_satellite(star_system):
    while True:
        try:
            planet_name = input("enter planet's name were search satellite")
            planet = star_system.search_planet(planet_name)
            break
        except ValueError:
            print("this planet not exist.Try again")
    name = input("enter name satellite")
    while True:
        try:
            speed = float(input("enter satellite's speed"))
            break
        except ValueError:
            print("not a valid speed")
    while True:
        try:
            mass = float(input("enter satellite mass"))
            break
        except ValueError:
            print("not a valid mass")
    while True:
        try:
            x = float(input("enter x satellite position"))
            y = float(input("enter y satellite position"))
            z = float(input("enter z satellite position"))
            break
        except ValueError:
            print("not a valid coordinates")
    while True:
        try:
            radius = float(input("enter satellite radius"))
            break
        except ValueError:
            print("not a valid radius")
    satellite = Satellite(name, speed, mass, x, y, z, radius, planet)
    star_system.add_satellite(satellite)


def search_asteroid(star_system):
    name = input("enter name asteroid")
    while True:
        try:
            speed = float(input("enter asteroid's speed"))
            break
        except ValueError:
            print("not a valid speed")
    while True:
        try:
            mass = float(input("enter asteroid mass"))
            break
        except ValueError:
            print("not a valid mass")
    while True:
        try:
            x = float(input("enter x asteroid position"))
            y = float(input("enter y asteroid position"))
            z = float(input("enter z asteroid position"))
            break
        except ValueError:
            print("not a valid coordinates")
    while True:
        try:
            radius = float(input("enter asteroid radius"))
            break
        except ValueError:
            print("not a valid radius")
    asteroid = Asteroid(name, speed, mass, x, y, z, radius)
    star_system.add_asteroid(asteroid)


def search_comets(star_system):
    name = input("enter name cometa")
    while True:
        try:
            speed = float(input("enter cometa's speed"))
            break
        except ValueError:
            print("not a valid speed")
    while True:
        try:
            mass = float(input("enter cometa mass"))
            break
        except ValueError:
            print("not a valid mass")
    while True:
        try:
            x = float(input("enter x cometa position"))
            y = float(input("enter y cometa position"))
            z = float(input("enter z cometa position"))
            break
        except ValueError:
            print("not a valid coordinates")
    while True:
        try:
            radius = float(input("enter cometa radius"))
            break
        except ValueError:
            print("not a valid radius")
    cometa = Cometa(name, speed, mass, x, y, z, radius, star=star_system.get_star())
    star_system.add_cometa(cometa)


def speed_planet(star_system: StarSystem):
    while True:
        try:
            planet_name = input("enter name planet")
            planet = star_system.search_planet(planet_name)
            break
        except ValueError:
            print("not a found planet. Try again")
    try:
        spacecraft_name = input("enter name spacecraft")
        spacecraft = star_system.search_spacecraft(spacecraft_name)
    except ValueError:
        print("not a found spacecraft")
        return
    print(spacecraft.speed_exploration(planet))


def modelling_orbits(star_system: StarSystem):
    while True:
        try:
            planet_name = input("enter name planet")
            planet = star_system.search_planet(planet_name)
            break
        except ValueError:
            print("not a found planet. Try again")
    try:
        spacecraft_name = input("enter name spacecraft")
        spacecraft = star_system.search_spacecraft(spacecraft_name)
    except ValueError:
        print("not a found spacecraft")
        return
    spacecraft.modeling_orbit(star_system.get_star(), planet)


if __name__ == '__main__':
    choose = 0
    system = StarSystem()
    if not os.path.isfile("star_system.pickle") or os.path.getsize("star_system.pickle") == 0:
        print("Creating star system")
        system = create_system()
    else:
        print("""
                Input number of operation:
                1 - Create system
                2 - Download exist system
                """)
        choose = int(input("Enter:"))
        match choose:
            case 1:
                system = create_system()
            case 2:
                with open("star_system.pickle", "rb") as file:
                    system = pickle.load(file)
                    system.get_info()
                print("Loaded successfully")
    while True:
        choose = 0
        print("""
        Input number of operation:
        1 - launch spacecraft
        2 - analysis planet atmosphere
        3 - analysis  spaceobject
        4 - modelling planet orbit
        5 - planet speed exploration
        6 - add satellite
        7 - add asteroid
        8 - add cometa
        9 - add planet
        10 - star system info
        11 - Save
        12 - Exit
        """)
        while True:
            try:
                choose = int(input("enter:"))
                break
            except ValueError:
                print("not correct")
        match choose:
            case 1:
                launch_spacecraft(system)
            case 2:
                analysis_planet(system)
            case 3:
                analysis_spaceobject(system)
            case 4:
                modelling_orbits(system)
            case 5:
                speed_planet(system)
            case 6:
                search_satellite(system)
            case 7:
                search_asteroid(system)
            case 8:
                search_comets(system)
            case 9:
                search_planet(system)
            case 10:
                system.get_info()
            case 11:
                system.save()
            case 12:
                break
