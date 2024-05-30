from star import Star
from asteroid import Asteroid


class Cometa(Asteroid):
    def __init__(self, name: str, speed: float, mass: float, x: float, y: float, z: float, radius: float,
                 star: Star = None):
        super().__init__(name,  speed, mass, x, y, z, radius)
        self.__star_orbit = star

    def get_star_orbit(self) -> Star:
        return self.__star_orbit

