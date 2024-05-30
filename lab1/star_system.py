from space_object import SpaceObject
from star import Star
from cometa import Cometa
from planet import Planet
from satellite import Satellite
from asteroid import Asteroid
from spacecraft import Spacecraft
import pickle


# хранит все данные о солнечной системе и выводит их
class StarSystem:
    def __init__(self,  star: Star = None, planets: list[Planet] = [], satellite: list[Satellite] = [],
                 asteroid: list[Asteroid] = [], cometa: list[Cometa] = [], spacecraft: list[Spacecraft] = []):
        self.__star = star
        self.__planets = planets
        self.__satellite = satellite
        self.__asteroids = asteroid
        self.__cometa = cometa
        self.__spacecraft = spacecraft

    def add_planet(self, planet: Planet):
        self.__planets.append(planet)

    def add_satellite(self, satellite: Satellite):
        self.__satellite.append(satellite)

    def add_asteroid(self, asteroid: Asteroid):
        self.__asteroids.append(asteroid)

    def add_cometa(self, cometa: Cometa):
        self.__cometa.append(cometa)

    def add_spacecraft(self, spacecraft: Spacecraft):
        self.__spacecraft.append(spacecraft)

    def search_planet(self, name: str) -> Planet:
        for planet in self.__planets:
            if planet.get_name() == name:
                return planet
        raise ValueError(f"not found")

    def search_space_object(self, name: str) -> SpaceObject:
        try:
            planet = self.search_planet(name)
            return planet
        except ValueError:
            for spaceobject in self.__satellite:
                if spaceobject.get_name() == name:
                    return spaceobject
            for spaceobject in self.__asteroids:
                if spaceobject.get_name() == name:
                    return spaceobject
            for spaceobject in self.__cometa:
                if spaceobject.get_name() == name:
                    return spaceobject
            if self.__star.get_name() == name:
                return self.__star
            raise ValueError(f"Not found")

    def search_spacecraft(self, name: str) -> Spacecraft:
        for spacecraft in self.__spacecraft:
            if spacecraft.get_name() == name:
                return spacecraft
        raise ValueError(f"not found")

    def get_info(self):
        print(f"Star: {self.__star.get_name()}")
        print("Planets: ")
        for planet in self.__planets:
            print(planet.get_name() + ",")
        print("Satellites: ")
        for satellite in self.__satellite:
            print(satellite.get_name()+",")
        print("Asteroids: ")
        for asteroid in self.__asteroids:
            print(asteroid.get_name() + ",")
        print("Cometies: ")
        for cometa in self.__cometa:
            print(cometa.get_name()+",")
        print("Spacecrafts: ")
        for spacecraft in self.__spacecraft:
            print(spacecraft.get_name()+",")

    def get_star(self):
        return self.__star

    def save(self):
        with open("star_system.pickle", "wb") as file:
            pickle.dump(self, file)
        print("Save successful!")
