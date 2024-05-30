# класс для всех естественных объектов солнечной системы
class SpaceObject(object):
    def __init__(self, name: str, speed: float, mass: float, x: float, y: float, z: float, radius: float,
                 atmosphere: list[float] = None):
        self.__name = name
        self.__speed = speed
        self.__mass = mass
        self.__x = x
        self.__y = y
        self.__z = z
        self.__radius = radius
        self.__gravity = 6.67408e-11*mass/radius**2
        self.__atmosphere = atmosphere

    def get_name(self):
        return self.__name

    def get_speed(self) -> float:
        return self.__speed

    def get_mass(self) -> float:
        return self.__mass

    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y

    def get_z(self) -> float:
        return self.__z

    def get_gravity(self) -> float:
        return self.__gravity

    def get_radius(self) -> float:
        return self.__radius

    def get_atmosphere(self) -> list[float]:
        return self.__atmosphere

    def get_info(self) -> dict:
        info = {'name': self.__name, 'speed': self.__speed, 'mass': self.__mass, 'gravity': self.__gravity,
                'radius': self.__radius, 'atmosphere': self.__atmosphere, 'coordinates': [self.__x, self.__y, self.__z]}
        return info
