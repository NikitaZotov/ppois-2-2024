from space_object import SpaceObject


class Spacecraft(object):
    def __init__(self, name: str,  planet: SpaceObject):
        self.__name = name
        self.__planet = planet

    def speed_exploration(self, planet: SpaceObject) -> float:
        return planet.get_speed()

    def modeling_orbit(self, space_object1: SpaceObject, space_object2: SpaceObject) -> float:
        x = space_object1.get_x()-space_object2.get_x()
        y = space_object1.get_y()-space_object2.get_y()
        z = space_object1.get_z()-space_object2.get_z()
        if (x**2 + y**2 + z**2)**0.5 == 0:
            raise Exception("It's one object")
        print(f'orbit of {space_object2.get_name()} is {(x**2 + y**2 + z**2)**0.5}')
        return (x**2 + y**2 + z**2)**0.5

    def analysis_planet(self, planet: SpaceObject):
        if planet.get_atmosphere() is None:
            print("This object don't have atmosphere yet")
        else:
            atmosphere = planet.get_atmosphere()

            atmospheres = (f'\natmosphere: \n 1 element:{atmosphere[0]}; \n 2 element:{atmosphere[1]},'
                           f'\n 3 element:{atmosphere[2]},\n 4 element:{atmosphere[3]},'
                           f'\n 5 element:{atmosphere[4]} \n')
            print(f'planet: {planet.get_name()}'+atmospheres)

    def analysis_space_object(self, space_object: SpaceObject):
        info = space_object.get_info()
        coordinate = f"\ncoordinate: x={info['coordinates'][0]}, y={info['coordinates'][1]}, z={info['coordinates'][2]}"
        atmosphere = ''
        if info['atmosphere'] is not None:
            atmosphere = (f'\natmosphere: \n 1 element:{info['atmosphere'][0]}; \n 2 element:{info['atmosphere'][1]},'
                          f'\n 3 element:{info['atmosphere'][2]},\n 4 element:{info['atmosphere'][3]},'
                          f'\n 5 element:{info['atmosphere'][4]} \n')
        else:
            atmosphere = "\ndon't have atmosphere\n"
        informate = (f"name:{info['name']};\nspeed: {info['speed']};\nmass: {info['mass']};"
                     f"\ngravity: {info['gravity']};")
        print(informate+atmosphere+coordinate)

    def get_name(self):
        return self.__name


if __name__ == '__main__':
    planet = SpaceObject('Earth', 6378137.0, 42, 3, 2, 4, 23)
    carts = Spacecraft('Earth', planet)
    carts.modeling_orbit(planet, planet)
